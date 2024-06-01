CREATE TRIGGER create_state
AFTER INSERT ON raw_data.Orden
FOR EACH ROW
EXECUTE FUNCTION create_state_func();

CREATE TRIGGER actualizar_estado
BEFORE INSERT ON summary_data.ordenes
FOR EACH ROW
EXECUTE FUNCTION trigger_actualizar_estado();

CREATE TRIGGER after_insert_summary_data
AFTER INSERT ON summary_data.ordenes
FOR EACH ROW
EXECUTE FUNCTION update_summary_data();

CREATE TRIGGER after_insert_estado
AFTER INSERT ON raw_data.estado
FOR EACH ROW
EXECUTE FUNCTION insert_estado_func();
