-- Script de inicialización de la base de datos
-- Este archivo se ejecuta automáticamente cuando se inicia el contenedor de PostgreSQL

-- Crear esquema UANL
CREATE SCHEMA IF NOT EXISTS uanl;

-- Crear tabla de operadores
CREATE TABLE IF NOT EXISTS uanl.operators (
  operator_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  email VARCHAR(255),
  phone VARCHAR(20),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla de clientes
CREATE TABLE IF NOT EXISTS uanl.clients (
  client_id SERIAL PRIMARY KEY,
  external_ref VARCHAR(64) NOT NULL UNIQUE,
  name VARCHAR(255),
  email VARCHAR(255),
  phone VARCHAR(20),
  address TEXT,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla de llamadas
CREATE TABLE IF NOT EXISTS uanl.calls (
  call_id BIGSERIAL PRIMARY KEY,
  call_label TEXT,
  operator_id INTEGER NOT NULL REFERENCES uanl.operators(operator_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  client_id INTEGER NOT NULL REFERENCES uanl.clients(client_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  call_date DATE NOT NULL,
  call_time TIME,
  duration_seconds INTEGER,
  conversation TEXT,
  call_type VARCHAR(50) DEFAULT 'incoming',
  status VARCHAR(50) DEFAULT 'completed',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla de tickets
CREATE TABLE IF NOT EXISTS uanl.tickets (
  ticket_id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'open',
  priority VARCHAR(50) DEFAULT 'medium',
  call_id BIGINT REFERENCES uanl.calls(call_id) ON UPDATE CASCADE ON DELETE SET NULL,
  assigned_operator_id INTEGER REFERENCES uanl.operators(operator_id) ON UPDATE CASCADE ON DELETE SET NULL,
  client_id INTEGER NOT NULL REFERENCES uanl.clients(client_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  watson_session_id VARCHAR(255),
  watson_metadata TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  resolved_at TIMESTAMP WITH TIME ZONE
);

-- Crear tabla de visitas programadas
CREATE TABLE IF NOT EXISTS uanl.scheduled_visits (
  visit_id SERIAL PRIMARY KEY,
  client_id INTEGER NOT NULL REFERENCES uanl.clients(client_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  operator_id INTEGER REFERENCES uanl.operators(operator_id) ON UPDATE CASCADE ON DELETE SET NULL,
  ticket_id INTEGER REFERENCES uanl.tickets(ticket_id) ON UPDATE CASCADE ON DELETE SET NULL,
  visit_date DATE NOT NULL,
  visit_time TIME,
  visit_type VARCHAR(100) DEFAULT 'maintenance',
  status VARCHAR(50) DEFAULT 'scheduled',
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla de notificaciones
CREATE TABLE IF NOT EXISTS uanl.notifications (
  notification_id SERIAL PRIMARY KEY,
  recipient_type VARCHAR(50) NOT NULL, -- 'client', 'operator', 'admin'
  recipient_id INTEGER NOT NULL,
  notification_type VARCHAR(100) NOT NULL, -- 'email', 'sms', 'push'
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'sent', 'failed'
  sent_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear tabla de reportes generados
CREATE TABLE IF NOT EXISTS uanl.reports (
  report_id SERIAL PRIMARY KEY,
  report_type VARCHAR(100) NOT NULL,
  report_name VARCHAR(255) NOT NULL,
  parameters TEXT, -- JSON con parámetros del reporte
  file_path VARCHAR(500),
  file_format VARCHAR(10),
  generated_by INTEGER REFERENCES uanl.operators(operator_id) ON UPDATE CASCADE ON DELETE SET NULL,
  status VARCHAR(50) DEFAULT 'generating',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  completed_at TIMESTAMP WITH TIME ZONE
);

-- Crear tabla de actividad de Watson
CREATE TABLE IF NOT EXISTS uanl.watson_activities (
  activity_id SERIAL PRIMARY KEY,
  session_id VARCHAR(255) NOT NULL,
  client_id INTEGER REFERENCES uanl.clients(client_id) ON UPDATE CASCADE ON DELETE SET NULL,
  user_input TEXT,
  bot_response TEXT,
  action_taken VARCHAR(100),
  context_data TEXT, -- JSON
  metadata TEXT, -- JSON
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crear índices para mejorar performance
CREATE INDEX IF NOT EXISTS idx_calls_date ON uanl.calls(call_date);
CREATE INDEX IF NOT EXISTS idx_calls_operator ON uanl.calls(operator_id);
CREATE INDEX IF NOT EXISTS idx_calls_client ON uanl.calls(client_id);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON uanl.tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_priority ON uanl.tickets(priority);
CREATE INDEX IF NOT EXISTS idx_tickets_client ON uanl.tickets(client_id);
CREATE INDEX IF NOT EXISTS idx_tickets_operator ON uanl.tickets(assigned_operator_id);
CREATE INDEX IF NOT EXISTS idx_tickets_watson_session ON uanl.tickets(watson_session_id);
CREATE INDEX IF NOT EXISTS idx_visits_date ON uanl.scheduled_visits(visit_date);
CREATE INDEX IF NOT EXISTS idx_notifications_status ON uanl.notifications(status);
CREATE INDEX IF NOT EXISTS idx_watson_session ON uanl.watson_activities(session_id);

-- Insertar datos de ejemplo
INSERT INTO uanl.operators (name, email, phone) VALUES 
('Ana García', 'ana.garcia@uanl.mx', '+52-555-0001'),
('Carlos López', 'carlos.lopez@uanl.mx', '+52-555-0002'),
('María González', 'maria.gonzalez@uanl.mx', '+52-555-0003')
ON CONFLICT (name) DO NOTHING;

INSERT INTO uanl.clients (external_ref, name, email, phone) VALUES 
('CLI-001', 'Empresa ABC', 'contacto@abc.com', '+52-555-1001'),
('CLI-002', 'Corporativo XYZ', 'info@xyz.com', '+52-555-1002'),
('CLI-003', 'Servicios 123', 'soporte@123.com', '+52-555-1003')
ON CONFLICT (external_ref) DO NOTHING;

-- Función para actualizar timestamp automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Crear triggers para actualizar updated_at
CREATE TRIGGER update_operators_updated_at BEFORE UPDATE ON uanl.operators 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON uanl.clients 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_calls_updated_at BEFORE UPDATE ON uanl.calls 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_tickets_updated_at BEFORE UPDATE ON uanl.tickets 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    
CREATE TRIGGER update_visits_updated_at BEFORE UPDATE ON uanl.scheduled_visits 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
