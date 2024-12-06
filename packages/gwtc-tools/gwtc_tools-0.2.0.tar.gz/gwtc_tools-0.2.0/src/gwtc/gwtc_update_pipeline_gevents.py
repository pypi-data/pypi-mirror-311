from gwtc.gwtc_gracedb import GWTCGraceDB
from .gwtc import update_far_and_pastro_in_smap, gwtc_update_pipeline_events
import logging
from optparse import OptionParser
import json
import time
import yaml

# setup verbose logs
logging.basicConfig(level=logging.INFO)


def get_super_events(client, g_event_ids, g_events=None):
    out = {}
    retry = set()
    if g_events is None:
        g_events = {
            event["graceid"]: event for event in client.events(" ".join(g_event_ids))
        }
    for gid in g_event_ids:
        res = g_events[gid]
        if res["superevent"] is not None:
            out[res["superevent"]] = {
                "pipelines": {res["pipeline"]: gid},
                "far": None,
                "pastro": None,
            }
            logging.info(
                f"associated super event {res['superevent']} with gevent {gid}"
            )
        else:
            logging.info(f"No super event found for gevent {gid}")
            retry.add(gid)
    return out, retry


def parse_command_line():
    parser = OptionParser()
    parser.add_option(
        "--group",
        type="string",
        default="CBC",
        help="Set the group name to upload. default CBC",
    )
    parser.add_option(
        "--search",
        type="string",
        default="AllSky",
        help="Set the search name to upload. default AllSky",
    )
    parser.add_option("--pipeline", type="string", help="Set the pipeline. required")
    parser.add_option(
        "--proxy-path", type="string", help="Set the path to find the proxy file"
    )
    parser.add_option(
        "--service-url",
        type="string",
        default="https://gracedb-test.ligo.org/api/",
        help="Set the gracedb service url. Default: https://gracedb-test.ligo.org/api/",
    )
    parser.add_option(
        "--number", type="str", default="4", help='Set the catalog number: default "4"'
    )
    parser.add_option(
        "--reset",
        action="store_true",
        help="Assume the current gevents should replace the pipelines gwtc events by deleting gevents entries for superevents not in the provided set. This is useful for completely replacing events for a given pipeline but should not be used for just updating some gevents. NOTE: This doesn't delete any gevents from any database, it simply removes gevents mappings in the catalog.",
    )
    parser.add_option(
        "--in-yaml",
        type="str",
        help="Specify the yaml file containing input coinc files and pastros",
    )
    parser.add_option(
        "--out-yaml",
        type="str",
        help="Specify the yaml file to output the processed inputs",
    )
    options, filenames = parser.parse_args()
    assert len(filenames) == 0
    for option in ("pipeline",):
        if getattr(options, option.replace("-", "_")) is None:
            raise ValueError(f"--{option} is required")

    return options


def main():
    options = parse_command_line()
    if options.in_yaml is not None:
        with open(options.in_yaml) as f:
            cfg = yaml.safe_load(f.read())
    else:
        cfg = []

    client = GWTCGraceDB(service_url=options.service_url, cred=options.proxy_path)

    g_event_ids = []
    for line in cfg:
        if "gid" in line:
            assert "coinc" not in line
            gid = line["gid"]
        else:
            resp = client.createEvent(
                options.group,
                options.pipeline,
                line["coinc"],
                search=options.search,
                offline=True,
            )
            gid = resp.json()["graceid"]
            line["gid"] = gid
            logging.info(f"Uploaded {gid}")
        g_event_ids.append(gid)

        if "pastro" in line and line["pastro"]:
            with open(line["pastro"]) as f:
                client.writeLog(
                    gid,
                    "Submitted the p-astro file",
                    filename="p_astro.json",
                    filecontents=f.read(),
                    tagname="p_astro",
                )

            logging.info(f"Uploaded {g_event_ids[-1]} pastro")
        if "extra" in line:
            for extra in line["extra"]:
                assert not (
                    set(extra) - set(("message", "filename", "tag_name", "displayName"))
                )
                assert "message" in extra and "filename" in extra
                client.writeLog(gid, **extra)
                logging.info(f"Uploaded {extra}")

    pmap = {}
    retry = set(g_event_ids)
    g_events = {}
    while len(retry) > 0:
        time.sleep(1)
        g_events = g_events | {
            event["graceid"]: event
            for event in client.events(" ".join(retry), count=500)
        }
        out, retry = get_super_events(client, retry, g_events=g_events)
        pmap.update(out)

    pmap = update_far_and_pastro_in_smap(client, pmap, g_events=g_events)

    logging.info(f"Uploading\n{json.dumps(pmap, indent=4)}")
    resp = gwtc_update_pipeline_events(
        client,
        pmap,
        options.pipeline,
        options.number,
        reset=options.reset,
        g_events=g_events,
    )
    logging.info(f"Created GWTC:\n{json.dumps(resp.json(), indent=4)}")

    if options.out_yaml is not None:
        with open(options.out_yaml, "w") as f:
            f.write(yaml.dump(cfg))
