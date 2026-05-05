# DuplicateFileKiller

Перезагрузить postgres
```
docker restart duplicate_file_killer_postgres
```

Удалить БД
```
docker exec -i duplicate_file_killer_postgres su postgres -c "dropdb -U duplicate_file_killer duplicate_file_killer"
```

Создать пустую БД
```
docker exec -i duplicate_file_killer_postgres su postgres -c "createdb -U duplicate_file_killer -O duplicate_file_killer duplicate_file_killer"
```
