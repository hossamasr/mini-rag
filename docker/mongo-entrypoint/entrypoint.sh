#!/usr/bin/env bash
echo "Creating mongo users..."
mongosh --authenticationDatabase admin --host localhost -u admin -p admin mini-rag --eval "db.createUser({user: 'devUser', pwd: 'devUserPass', roles: [{role: 'readWrite', db: 'app_db_name'}]});"
echo "Mongo users created."