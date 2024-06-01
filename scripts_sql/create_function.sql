CREATE OR REPLACE FUNCTION get_estado_actualizado(orden_id_param INT)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    estado_actual TEXT;
BEGIN
    SELECT estado
    INTO estado_actual
    FROM raw_data.orden
    WHERE id = orden_id_param
    ORDER BY fecha_actualizacion DESC
    LIMIT 1;
    
    RETURN estado_actual;
END;
$$;

CREATE OR REPLACE FUNCTION update_delivered_at_func()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE raw_data.Orden
    SET delivered_at = CASE
        WHEN NEW.estado = (SELECT estado 
                            FROM raw_data.Estado 
                            WHERE orden_id = NEW.orden_id
                            ORDER BY id DESC
                            LIMIT 1) AND NEW.estado = 'entregado' -- Reemplaza 3 por el estado de entrega
        THEN NEW.timestamp
        ELSE delivered_at
    END
    WHERE id = NEW.orden_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION trigger_actualizar_estado()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.estado = get_estado_actualizado(NEW.orden_id);
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION create_state_func()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO raw_data.Estado (orden_id, estado, tiempo_estado)
    VALUES (NEW.id, 1, '0');
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_delivered_at_func()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE raw_data.Orden
    SET delivered_at = CASE
        WHEN NEW.estado = 'entregado'
        THEN NEW.timestamp
        ELSE delivered_at
    END
    WHERE id = NEW.orden_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION update_summary_data()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE summary_data.ordenes
    SET 
        fecha_creacion = (SELECT DATE(created_at) FROM raw_data.Orden WHERE id = NEW.orden_id),
        fecha_entrega = (SELECT DATE(delivered_at) FROM raw_data.Orden WHERE id = NEW.orden_id),
        nombre_operador = (SELECT nombre_operador FROM raw_data.Orden WHERE id = NEW.orden_id),
        estado = (
            SELECT estado 
            FROM raw_data.Estado 
            WHERE orden_id = NEW.orden_id 
            ORDER BY timestamp DESC 
            LIMIT 1
        )
    WHERE orden_id = NEW.orden_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;




