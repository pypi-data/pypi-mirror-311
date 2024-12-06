A very simple OVH dyndns client to workaround difficulties with Ubiquity unadyn...

A config file is to be created at `~/.udyndns.json`

```json lines
{
  "my_first_domain.net": {
    "unifi": {
      "host": "ugw",
      "port": 8443,
      "username": "ugw_user_to_retrieve_wan_ip",
      "password": "ugw_password_to_retrieve_wan_ip"
    },
    "ovh": {
      "username": "my_dyndns_username",
      "password": "my_dyndns_password"
    }
  },
  "my_second_domain.net": {
    "unifi": {
      "host": "udm",
      "port": 443,
      "username": "udm_user_to_retrieve_wan_ip",
      "password": "udm_password_to_retrieve_wan_ip"
    },
    "ovh": {
      "username": "my_other_dyndns_username",
      "password": "my_other_dyndns_password"
    }
  }
}
```

Running this command every hour can be done with the following crontab:

`0 * * * * python3 -m udyndns`