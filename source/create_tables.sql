-- Es importante que el orden de los DROPs se mantenga lo mismo 
DROP TABLE IF EXISTS MedioDuenoRelacion;
DROP TABLE IF EXISTS NoticiaCitadoRelacion;
DROP TABLE IF EXISTS Noticias;
DROP TABLE IF EXISTS Citados;
DROP TABLE IF EXISTS Notoriedades;
DROP TABLE IF EXISTS Medios;
DROP TABLE IF EXISTS Duenos;

CREATE TABLE IF NOT EXISTS Medios(
  url VARCHAR(255) PRIMARY KEY,
  nombre VARCHAR(200) NOT NULL,
  ciudad VARCHAR(50) NOT NULL,
  idioma VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS Duenos(
  id INT AUTO_INCREMENT PRIMARY KEY, 
  nombre VARCHAR(100) NOT NULL,
  fecha_cargo DATE NOT NULL,
  categoria VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS MedioDuenoRelacion(
  medio_url VARCHAR(255) NOT NULL,
  dueno_id INT NOT NULL,
  FOREIGN KEY (medio_url) REFERENCES Medios(url),
  FOREIGN KEY (dueno_id) REFERENCES Duenos(id),
  UNIQUE (medio_url, dueno_id)
);

CREATE TABLE IF NOT EXISTS Noticias(
  url VARCHAR(255) PRIMARY KEY,
  fecha_publicacion DATETIME NOT NULL,
  titulo MEDIUMTEXT NOT NULL,
  categoria VARCHAR(50) NOT NULL,
  contenido MEDIUMTEXT NOT NULL,
  medio_url VARCHAR(255) NOT NULL,
  FOREIGN KEY (medio_url) REFERENCES Medios(url)
);

CREATE TABLE IF NOT EXISTS Notoriedades(
  url VARCHAR(255) PRIMARY KEY,
  fecha_nacimiento DATE NOT NULL,
  -- Es popularidad un INT o algún otro tipo?
  popularidad INT NOT NULL, 
  profesion VARCHAR(50) NOT NULL,
  nacionalidad VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Citados(
  id INT AUTO_INCREMENT PRIMARY KEY, 
  nombre VARCHAR(200) NOT NULL,
  notoriedad_url VARCHAR(255),
  FOREIGN KEY (notoriedad_url) REFERENCES Notoriedades(url)
);

CREATE TABLE IF NOT EXISTS NoticiaCitadoRelacion(
  noticia_url VARCHAR(255) NOT NULL,
  citado_id INT NOT NULL,
  FOREIGN KEY (noticia_url) REFERENCES Noticias(url),
  FOREIGN KEY (citado_id) REFERENCES Citados(id),
  UNIQUE (noticia_url, citado_id)
);

