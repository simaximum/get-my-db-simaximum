### Where is the endpoint hosted?

https://get-my-db-simaximum-2.herokuapp.com/stats

### How do I test sending a payload?

In python:

```python
import requests

json_ex = {"token":"azerty", "customer":"tf1", "content":"kohlanta", "timespan":30000, "p2p":456, "cdn":123, "sessionDuration": 120000}

res = requests.post('https://get-my-db-simaximum-2.herokuapp.com/stats', json=json_ex)

res.ok

res.text
```


### How do I query the table?

In my shell:

```shell
heroku pg:psql --app get-my-db-simaximum-2

select * from stats;
```