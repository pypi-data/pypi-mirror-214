# webhdfspy


## Descripción 📄

El webhdfspy es una biblioteca que proporciona una interfaz conveniente para interactuar con WebHDFS, el servicio de sistema de archivos distribuido de Hadoop a través de HTTP. Este wrapper simplifica el proceso de realizar operaciones como crear archivos, leer y escribir datos, crear directorios y administrar permisos en el clúster Hadoop utilizando la API de WebHDFS.

Características principales:

- Conexión y autenticación sencillas con clústeres Hadoop a través de HTTP.
- Métodos simples y intuitivos para realizar operaciones básicas de sistema de archivos, como crear, leer y escribir archivos, así como también crear y administrar directorios.
- Compatibilidad con las operaciones más comunes de WebHDFS, como agregar datos a un archivo existente, obtener información sobre archivos y directorios, cambiar permisos y propietarios, y más.
- Manejo de errores y excepciones para una experiencia de uso robusta y segura.

El webhdfspy es una herramienta útil para desarrolladores que deseen interactuar con clústeres Hadoop y realizar operaciones en HDFS de forma sencilla y eficiente. 

## Example

Agregar el siguiente codigo para ejecutar web app con ejemplo de uso
```
    from webhdfs_py import example

    if __name__ == "__main__":
        example.run()
```

### TODO

- [ ] Generarlizar el proyecto.

### In Progress

- [ ] Implementar para instalar con PIP

### Done ✓

- [x] Generar el primer desarrollo
- [X] Implementar 



##  Tabla de Métodos y Descripciones 📑

| Método | Descripción |
| ------ | ----------- |
| create_file | Crea un nuevo archivo en HDFS en la ruta especificada |
| append_file | Realiza un append de datos en un archivo dentro de HDFS |
| read_file | Abre el archivo completo (permite guardar en destino), tener en cuenta el peso del archivo |
| stream_file | Genera un iterable del archivo permitiendo guardar los datos del archivo en bloques |
| make_dir | Crea un nuevo directorio |
| rename_file_dir | Renombra un archivo o un directorio |
| delete_file_dir | Elimina un archivo o directorio |
| get_file_dir_status | Retorna en JSON el estado de un archivo o directorio (Permisos, replicaciones, etc.) |
| get_content_summary | Retorna en JSON un resumen de un directorio en específico (Cantidad de archivos, peso, cantidad de archivos) |
| get_file_checksum | Retorna en JSON el checksum y el algoritmo |
| list_dir | Retorna en JSON el estado de los archivos o directorios de la ruta en HDFS |
| exists_file_dir | Retorna BOOL si existe el directorio o archivo |
| set_permission | Setea los permisos de un archivo o directorio |
| set_owner | Setea el owner y/o el grupo |


La documentacion se puede revisar en:

[WebHDFS REST API](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/WebHDFS.html)


## Developer

**Erik Alejandro Abdala**