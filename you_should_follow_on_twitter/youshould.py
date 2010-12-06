# -*- coding: utf-8 -*-
import getpass
import sys
import twitter

if __name__ == '__main__':
    user = input("Username: ")
    password = getpass.getpass("Password: ")
    print 'Connecting to twitter...'
    try:
        api = twitter.Api(user, password)
    except:
        print 'Error connecting to twitter api. Check your connection, ' \
                'your username and password and try again.'
        sys.exit(1)
    print 'Fetching friends...'
    try:
        amigos = api.GetFriends()
    except:
        print 'Error fetching friends'
        sys.exit(1)
    primeros = [ primero._screen_name for primero in amigos ]
    print 'Friends fetched. Obtaining second-level contacts...'
    segundos = []
    for primero in primeros:
        try:
            second_level = api.GetFriends(primero)
            for segundo in second_level:
                segundos.append(segundo._screen_name)
        except:
            print 'Error fetching friends for %s' % primero._screen_name
    if len(segundos) == 0:
        print 'No recommendations can be done, no second-level users found'
        exit(1)
    print 'Done traversing. These are our recommendations:'
    recomienda = dict()
    for segundo in segundos:
        if segundo not in primeros and segundo != user:
            if lista.has_key(segundo):
                lista[segundo] += 1
            else:
                lista.update([(segundo, 1)])
    ordenados = [ (lista[usuario], usuario) for usuario in recomienda ]
    ordenados.sort()
    ordenados.reverse()
    for sugerencia in ordenados[0:9]:
        print "\tYou should follow '%s', for %d of your friends are "\
                "currently following him/her."%(sugerencia[1], sugerencia[0])
