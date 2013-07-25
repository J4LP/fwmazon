import sys, json
from account.models import User
from eve.models import APIKey, Character


def main():
    data = parse_args()
    try:
        user = User.objects.get(username=data.username)
    except User.DoesNotExist:
        user = create_user(data)
    else:
        update_user(user, data)


def parse_args():
    try:
        data = json.loads(sys.argv[1])
    except:
        print json.dumps({'status': 'Error, could not parse arguments'})
        sys.exit(1)
    else:
        return data


def create_user(data):
    try:
        user = User.objects.create_user(data.username, data.email, data.password)
        api = APIKey(id=data.key_id, vcode=data.key_vcode, user=user)
        api.save()
        character = Character(id=data.character_id, name=data.character_name, user=user)
        character.save()
    except:
        print json.dumps({'status': 'error', 'message': 'Could not create user and save user details'})
        sys.exit(1)
    else:
        return user


def update_user(user, data):
    try:
        user.email = data.email
        user.password = data.password
        user.save()
        api = user.api
        api.id = data.key_id
        api.vcode = data.key_vcode
        api.save()
    except:
        print json.dumps({'status': 'error', 'message': 'Could not update user details'})
        sys.exit(1)

if __name__ == "__main__":
    main()