-- ============================================
-- CREACIÓN DE TABLA PRINCIPAL
-- ============================================
CREATE TABLE IF NOT EXISTS Documentos (
    ID_Documento INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre_Archivo TEXT NOT NULL,
    Tipo_Formato TEXT CHECK(Tipo_Formato IN ('Word','PDF','Excel','CSV')),
    Ruta_Archivo TEXT NOT NULL,
    Fecha_Registro DATE DEFAULT (DATE('now')),
    Autor TEXT,
    Categoria TEXT,
    Palabras_Clave TEXT
);

-- ============================================
-- INSERCIÓN DE REGISTROS DE EJEMPLO
-- ============================================
INSERT INTO Documentos (Nombre_Archivo, Tipo_Formato, Ruta_Archivo, Autor, Categoria, Palabras_Clave)
VALUES 
('Informe_Q1.pdf', 'PDF', '/documentos/2026/informe_q1.pdf', 'Christian Lozada', 'Informe', 'ventas, trimestral'),
('Planilla_Junio.xlsx', 'Excel', '/documentos/2026/planilla_junio.xlsx', 'RRHH', 'Planilla', 'sueldos, junio'),
('Contrato_Laboral.docx', 'Word', '/documentos/2026/contrato_laboral.docx', 'Legal', 'Contrato', 'empleado, contrato'),
('Datos_Clientes.csv', 'CSV', '/documentos/2026/datos_clientes.csv', 'Marketing', 'Base de datos', 'clientes, contactos'),
('Reporte_Finanzas.pdf', 'PDF', '/documentos/2026/reporte_finanzas.pdf', 'Contabilidad', 'Informe', 'finanzas, anual'),
('Inventario_Julio.xlsx', 'Excel', '/documentos/2026/inventario_julio.xlsx', 'Logística', 'Inventario', 'productos, stock');

-- ============================================
-- OPTIMIZACIÓN: CREACIÓN DE ÍNDICES
-- ============================================
-- Índice para acelerar búsquedas por palabras clave
CREATE INDEX IF NOT EXISTS idx_palabras ON Documentos(Palabras_Clave);

-- Índice para búsquedas rápidas por categoría
CREATE INDEX IF NOT EXISTS idx_categoria ON Documentos(Categoria);

-- ============================================
-- CONSULTAS DE EJEMPLO
-- ============================================

-- 1. Ver todos los documentos registrados
SELECT * FROM Documentos;

-- 2. Buscar documentos PDF relacionados con "ventas"
SELECT Nombre_Archivo, Ruta_Archivo, Fecha_Registro
FROM Documentos
WHERE Tipo_Formato = 'PDF'
AND Palabras_Clave LIKE '%ventas%';

-- 3. Buscar documentos de la categoría "Planilla"
SELECT Nombre_Archivo, Tipo_Formato, Ruta_Archivo
FROM Documentos
WHERE Categoria = 'Planilla';

-- 4. Buscar documentos creados por "Legal"
SELECT Nombre_Archivo, Tipo_Formato, Ruta_Archivo
FROM Documentos
WHERE Autor = 'Legal';

-- 5. Contar cuántos documentos hay por tipo de formato
SELECT Tipo_Formato, COUNT(*) AS Total
FROM Documentos
GROUP BY Tipo_Formato;

-- 6. Últimos documentos registrados (ordenados por fecha)
SELECT Nombre_Archivo, Tipo_Formato, Fecha_Registro
FROM Documentos
ORDER BY Fecha_Registro DESC;
-- Crear tabla principal de documentos
CREATE TABLE Documentos (
    ID_Documento INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre_Archivo TEXT NOT NULL,
    Tipo_Formato TEXT CHECK(Tipo_Formato IN ('Word','PDF','Excel','CSV')),
    Ruta_Archivo TEXT NOT NULL,
    Fecha_Registro DATE DEFAULT (DATE('now')),
    Autor TEXT,
    Categoria TEXT,
    Palabras_Clave TEXT
);

-- Insertar registros de ejemplo
INSERT INTO Documentos (Nombre_Archivo, Tipo_Formato, Ruta_Archivo, Autor, Categoria, Palabras_Clave)
VALUES 
('Informe_Q1.pdf', 'PDF', '/documentos/2026/informe_q1.pdf', 'Christian Lozada', 'Informe', 'ventas, trimestral'),
('Planilla_Junio.xlsx', 'Excel', '/documentos/2026/planilla_junio.xlsx', 'RRHH', 'Planilla', 'sueldos, junio'),
('Contrato_Laboral.docx', 'Word', '/documentos/2026/contrato_laboral.docx', 'Legal', 'Contrato', 'empleado, contrato'),
('Datos_Clientes.csv', 'CSV', '/documentos/2026/datos_clientes.csv', 'Marketing', 'Base de datos', 'clientes, contactos');

-- Consultas de ejemplo
-- Buscar PDFs relacionados con ventas
SELECT Nombre_Archivo, Ruta_Archivo, Fecha_Registro
FROM Documentos
WHERE Tipo_Formato = 'PDF'
AND Palabras_Clave LIKE '%ventas%';

-- Buscar documentos de la categoría Planilla
SELECT Nombre_Archivo, Tipo_Formato, Ruta_Archivo
FROM Documentos
WHERE Categoria = 'Planilla';
