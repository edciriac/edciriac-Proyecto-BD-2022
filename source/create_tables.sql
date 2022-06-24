CREATE TABLE IF NOT EXISTS Medios(
  id INT AUTO_INCREMENT PRIMARY KEY, 
  nombre VARCHAR(50) NOT NULL,
  ciudad VARCHAR(50) NOT NULL,
  url VARCHAR(100) NOT NULL,
  idioma VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS Duenos(
  id INT AUTO_INCREMENT PRIMARY KEY, 
  nombre VARCHAR(20) NOT NULL,
  fecha_cargo DATE NOT NULL,
  categoria VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS MedioDuenoRelacion(
  medio_id INT NOT NULL,
  dueno_id INT NOT NULL,
  FOREIGN KEY (medio_id) REFERENCES Medios(id),
  FOREIGN KEY (dueno_id) REFERENCES Duenos(id),
  UNIQUE (medio_id, dueno_id)
);

CREATE TABLE IF NOT EXISTS Noticias(
  id INT AUTO_INCREMENT PRIMARY KEY, 
  url VARCHAR(100) NOT NULL,
  fecha_publicacion DATETIME NOT NULL,
  titulo VARCHAR(50) NOT NULL,
  categoria VARCHAR(20) NOT NULL,
  contenido MEDIUMTEXT NOT NULL,
  medio_id INT NOT NULL,
  FOREIGN KEY (medio_id) REFERENCES Medios(id)
);

CREATE TABLE IF NOT EXISTS Notoriedades(
  id INT AUTO_INCREMENT PRIMARY KEY, 
  url VARCHAR(100) NOT NULL,
  fecha_nacimiento DATE NOT NULL,
  -- Es popularidad un INT o algún otro tipo?
  popularidad INT NOT NULL, 
  profesion VARCHAR(20) NOT NULL,
  nacionalidad VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS Citados(
  id INT AUTO_INCREMENT PRIMARY KEY, 
  nombre VARCHAR(50) NOT NULL,
  notoriedad_id INT,
  FOREIGN KEY (notoriedad_id) REFERENCES Notoriedades(id)
);

CREATE TABLE IF NOT EXISTS NoticiaCitadoRelacion(
  noticia_id INT NOT NULL,
  citado_id INT NOT NULL,
  FOREIGN KEY (noticia_id) REFERENCES Noticias(id),
  FOREIGN KEY (citado_id) REFERENCES Citados(id),
  UNIQUE (noticia_id, citado_id)
);

