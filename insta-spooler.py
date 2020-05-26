#!/usr/bin/env python3


import argparse
import requests


from instagram_private_api import Client, ClientCompatPatch


new_app_version = '10.3.2'
new_sig_key = '5ad7d6f013666cc93c88fc8af940348bd067b68f0dce3c85122a923f4f74b251'
new_key_ver = '4'           # does not freq change
new_ig_capa = '3ToAAA=='    # does not freq change


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--password-file", type=argparse.FileType("r"), required=True)
    args = parser.parse_args()

    if not args.password_file:
        print("Valid password file must exist!")
        raise SystemExit

    with args.password_file as fi:
        password = fi.read().strip()


    api = None


    api = Client(
        args.user,
        password,

        auto_patch=True, drop_incompat_keys=False,

        app_version=new_app_version,
        signature_key=new_sig_key,
        key_version= new_key_ver,
        ig_capabilities=new_ig_capa
    )

#   except Exception as e:
#       print(dir(e))
#       print(e.challenge_url)
#       requests.get(e.challenge_url)


    print(api.settings)
