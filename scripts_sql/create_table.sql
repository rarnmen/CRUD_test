CREATE SCHEMA raw_data;

CREATE DOMAIN estado_envio AS TEXT
CHECK (VALUE IN ('creado','asignado', 'en_transito', 'entregado', 'cancelado'));

CREATE TABLE raw_data.Orden (
    id SERIAL PRIMARY KEY,
    ubicacion TEXT NOT NULL,
    nombre_cliente TEXT NOT NULL,
    nombre_operador TEXT NOT NULL,
    productos TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    delivered_at TIMESTAMP
);

CREATE TABLE raw_data.Estado (
    id SERIAL PRIMARY KEY,
    orden_id INTEGER NOT NULL,
    estado estado_envio NOT NULL,
    tiempo_estado FLOAT ,
    timestamp TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (orden_id) REFERENCES raw_data.orden(id)
);

CREATE SCHEMA summary_data;

CREATE TABLE summary_data.ordenes (
    id SERIAL PRIMARY KEY,
    orden_id INTEGER UNIQUE, --
    fecha_creacion date, -- tomar de la tabla orden
    fecha_entrega date, -- tomar de la tabla orden
    estado estado_envio, -- tomar de la tabla estado tomando el valor del registro más reciente
    nombre_operador TEXT, 
    latitud FLOAT NOT NULL, 
    longitud FLOAT NOT NULL,
    tiempo_de_entrega INTEGER,
    FOREIGN KEY (orden_id) REFERENCES raw_data.orden(id)

);

CREATE TABLE summary_data.productos (
    id SERIAL PRIMARY KEY,
    orden_id INTEGER NOT NULL, -- tomar de registros
    producto_id INTEGER NOT NULL, -- separar productos idefnticatos
    fecha_entrega date, --tomar de la tabla orden
    FOREIGN KEY (orden_id) REFERENCES raw_data.orden(id)
);





