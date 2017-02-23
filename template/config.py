from timer import timed
import credstash
import json
import sys

def load_config(conf):
    with open(conf, 'r') as f:
        return json.loads(f.read())

def get_secret(key):
    get_env = lambda k: k.split('.')[0]
    get_table = lambda k: get_env(k)+'-credential-store' \
        if get_env(k) in ['prod', 'stage'] else 'credential-store'
    stringy = lambda x: type(x) in [str, unicode]
    if stringy(key) and key.startswith('credstash--'):
        try:
            credstash_key = key[11:]
            return credstash.getSecret(credstash_key, region='us-east-1',
                                       context={'env': get_env(credstash_key)},
                                       table=get_table(credstash_key))
        except:
            return ''
    else:
        return key

def configure(conf):
    return dict(map(lambda x: (x[0], get_secret(x[1])), conf.items()))

def auto_configure(conf):
    not_coll = lambda xs: all(type(x) not in [list, dict]
                              for x in map(lambda y: y[1], xs.items()))
    if type(conf) == dict and not_coll(conf):
        return configure(conf)
    elif type(conf) == dict:
        return dict(map(lambda x: (x[0], auto_configure(x[1])), conf.items()))
    elif type(conf) == list:
        return map(auto_configure, conf)
    else:
        return conf

def validate_schema(schema):
    print('validating metagraph_schema...')
    overlap = lambda xs, ys: len(set(xs) & set(ys)) > 0
    overlapping = filter(lambda t: overlap(t['transferable_state_keys'],
                                           t['universal_identity_keys']),
                         schema['tables'])
    if len(overlapping) > 0:
        print('Your metagraph_schema is bad!')
        print('The following tables are improperly configured: {}'
              .format(str(map(lambda t: t['name'], overlapping))))
        sys.exit(1)
    print('metagraph_schema validation successful!')
    return schema

@timed
def reconfigure(app_conf=None):
    reconf = lambda: \
        (auto_configure(app_conf if app_conf is not None else
                        load_config('conf/config.json')),
         validate_schema(load_config('resources/metagraph_schema.json')))
    global CONF
    global SCHEMA
    CONF, SCHEMA = reconf()

CONF = {}
SCHEMA = {}
reconfigure()
