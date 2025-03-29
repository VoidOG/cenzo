import os

API_ID = int(os.getenv("API_ID", "26075878"))
API_HASH = os.getenv("API_HASH", "7146213fe4324fcaca1bb6be7a2aef33")
SESSION_STRING = os.getenv("SESSION_STRING", "1BVtsOKEBu2HCc9Eh-Mz7JFIUiJXp0iUQL8ea9-X3aUsakn1-5tRjq0QsC0U3iFjA3Loes2FgU4_ktGKe7a7vAdjg81WiNvIZe1xUvSCJRPUgdJmlGDVFwqfq4Dc8hCVPnlbJGuM4A6GBW8tA62kIdbiwrV2pkbpR9aOY40gupNW3NJrQog-yLlO0_MwkbJzQgdes-EM4ghSJrHsk8i2Qt7aORd9np2YADF4Jj_YJHnxC9lPgPOYWuEJzwT8sV6wwLfjcpqbhus4bE1U0z84LqchTfl1ZQbaSDGOLHuPXwdmCysP3B03NAcjG4NNm16080oNYq5jkFhOrH_HsiRQ5GFRH9olkeHQ=")  # Telethon string session

DELAY = int(os.getenv("DELAY", "3600"))  # Delay (in seconds) between forwards
