-- Es importante que el orden de los DROPs se mantenga lo mismo 
DROP TABLE IF EXISTS MedioDuenoRelacion;
DROP TABLE IF EXISTS NoticiaPersonaRelacion;
DROP TABLE IF EXISTS Noticias;
DROP TABLE IF EXISTS Personas;
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

CREATE TABLE IF NOT EXISTS Personas(
  nombre VARCHAR(255) PRIMARY KEY,
  wikipedia_url VARCHAR(255),
  fecha_nacimiento DATE,
  popularidad INT,
  profesion VARCHAR(50),
  nacionalidad VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS NoticiaPersonaRelacion(
  noticia_url VARCHAR(255) NOT NULL,
  persona_nombre VARCHAR(255) NOT NULL,
  FOREIGN KEY (noticia_url) REFERENCES Noticias(url),
  FOREIGN KEY (persona_nombre) REFERENCES Personas(nombre),
  UNIQUE (noticia_url, persona_nombre)
);

