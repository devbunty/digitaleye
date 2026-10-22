from tests.conftest import make_heartbeat


def send(client, **kwargs):
    return client.post("/heartbeat", json=make_heartbeat(**kwargs))


def test_root_reports_application_name(client):
    body = client.get("/").get_json()
    assert body["application"] == "Digital Eye"
    assert body["status"] == "Running"


def test_heartbeat_registers_host(client):
    assert send(client).status_code == 200

    hosts = client.get("/hosts").get_json()
    assert [h["hostname"] for h in hosts] == ["web-01"]
    assert hosts[0]["is_demo"] is False
    assert hosts[0]["status"] == "Online"
    assert hosts[0]["last_seen"].endswith("+00:00")  # explicit UTC offset


def test_heartbeat_rejects_bad_payloads(client):
    assert client.post("/heartbeat", json={}).status_code == 400
    assert client.post("/heartbeat", json={"system": {"hostname": "x"}}).status_code == 400

    traversal = make_heartbeat(hostname="../evil")
    assert client.post("/heartbeat", json=traversal).status_code == 400


def test_new_host_is_online_and_in_dashboard(client):
    send(client)

    summary = client.get("/dashboard/summary").get_json()
    assert summary["total_hosts"] == 1
    assert summary["online_hosts"] == 1
    assert summary["security_health"] == 100.0

    resources = client.get("/dashboard/resources").get_json()
    assert resources[0]["status"] == "Online"
    assert resources[0]["cpu"] == 12.5


def test_demo_host_lifecycle(client):
    created = client.post("/hosts/demo", json={"hostname": "demo-1"})
    assert created.status_code == 201
    assert client.post("/hosts/demo", json={"hostname": "demo-1"}).status_code == 409
    assert client.post("/hosts/demo", json={}).status_code == 400

    assert client.delete("/hosts/demo-1").status_code == 200
    assert client.delete("/hosts/demo-1").status_code == 404


def test_real_hosts_cannot_be_deleted(client):
    send(client)
    assert client.delete("/hosts/web-01").status_code == 403


def test_assets_endpoints(client):
    send(client)
    for url in ("/assets", "/assets/hosts"):
        assets = client.get(url).get_json()
        assert assets[0]["hostname"] == "web-01"
        assert assets[0]["status"] == "Online"

    summary = client.get("/assets/summary").get_json()
    assert summary == {"total_hosts": 1, "online": 1, "offline": 0, "linux": 1, "windows": 0}


def test_analytics_shape(client):
    client.post("/hosts/demo", json={"hostname": "demo-1"})
    client.post("/hosts/demo", json={"hostname": "demo-2"})

    data = client.get("/analytics?hours=24").get_json()
    assert data["scope"] == "fleet"
    assert data["summary"]["monitored_hosts"] == 2
    assert data["by_severity_by_host"] is not None  # fleet view compares hosts

    single = client.get("/analytics?hostname=demo-1").get_json()
    assert single["scope"] == "demo-1"
    assert single["by_severity_by_host"] is None


def test_incident_lookup(client):
    client.post("/hosts/demo", json={"hostname": "demo-1"})

    incidents = client.get("/incidents").get_json()
    assert len(incidents) == 2

    one = client.get(f"/incidents/{incidents[0]['id']}")
    assert one.status_code == 200
    assert client.get("/incidents/99999").status_code == 404

    open_only = client.get("/incidents?status=Open").get_json()
    assert all(i["status"] == "Open" for i in open_only)
