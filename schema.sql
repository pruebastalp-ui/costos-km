CREATE DATABASE IF NOT EXISTS costos_mvp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE costos_mvp;

CREATE TABLE IF NOT EXISTS grupos_tarifarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(20) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  orden INT NOT NULL
);

CREATE TABLE IF NOT EXISTS definiciones_parametros (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(100) NOT NULL UNIQUE,
  modulo VARCHAR(50) NOT NULL,
  hoja_origen VARCHAR(100) NOT NULL,
  fila_origen INT NOT NULL,
  descripcion VARCHAR(255) NOT NULL,
  unidad VARCHAR(30) NULL,
  editable TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS valores_base (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  parametro_id INT NOT NULL,
  grupo_id INT NOT NULL,
  valor DECIMAL(18,6) NOT NULL,
  UNIQUE KEY uq_base_param_grupo (parametro_id, grupo_id),
  CONSTRAINT fk_base_param FOREIGN KEY (parametro_id) REFERENCES definiciones_parametros(id),
  CONSTRAINT fk_base_grupo FOREIGN KEY (grupo_id) REFERENCES grupos_tarifarios(id)
);

CREATE TABLE IF NOT EXISTS escenarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL UNIQUE,
  descripcion TEXT NULL,
  creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado_en DATETIME NOT NULL,
  activo TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS valores_escenario (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  escenario_id INT NOT NULL,
  parametro_id INT NOT NULL,
  grupo_id INT NOT NULL,
  valor DECIMAL(18,6) NOT NULL,
  UNIQUE KEY uq_escenario_param_grupo (escenario_id, parametro_id, grupo_id),
  CONSTRAINT fk_ve_escenario FOREIGN KEY (escenario_id) REFERENCES escenarios(id) ON DELETE CASCADE,
  CONSTRAINT fk_ve_param FOREIGN KEY (parametro_id) REFERENCES definiciones_parametros(id),
  CONSTRAINT fk_ve_grupo FOREIGN KEY (grupo_id) REFERENCES grupos_tarifarios(id)
);

CREATE TABLE IF NOT EXISTS definiciones_resultados (
  id INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(100) NOT NULL UNIQUE,
  orden INT NOT NULL,
  descripcion VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS resultados_base (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  resultado_id INT NOT NULL,
  grupo_id INT NOT NULL,
  valor DECIMAL(18,6) NOT NULL,
  UNIQUE KEY uq_res_base (resultado_id, grupo_id),
  CONSTRAINT fk_rb_resultado FOREIGN KEY (resultado_id) REFERENCES definiciones_resultados(id),
  CONSTRAINT fk_rb_grupo FOREIGN KEY (grupo_id) REFERENCES grupos_tarifarios(id)
);

CREATE TABLE IF NOT EXISTS resultados_escenario (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  escenario_id INT NOT NULL,
  resultado_id INT NOT NULL,
  grupo_id INT NOT NULL,
  valor DECIMAL(18,6) NOT NULL,
  calculado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_res_escenario (escenario_id, resultado_id, grupo_id),
  CONSTRAINT fk_re_escenario FOREIGN KEY (escenario_id) REFERENCES escenarios(id) ON DELETE CASCADE,
  CONSTRAINT fk_re_resultado FOREIGN KEY (resultado_id) REFERENCES definiciones_resultados(id),
  CONSTRAINT fk_re_grupo FOREIGN KEY (grupo_id) REFERENCES grupos_tarifarios(id)
);
