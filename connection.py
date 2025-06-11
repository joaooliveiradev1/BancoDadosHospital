import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')

def conectar():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='12345678',
        database='hospital_db'
    )

def popular_departamentos(cursor, quantidade):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO Departamento (id_departamento, nome_departamento, descricao) VALUES (%s, %s, %s)",
            (i, fake.job(), fake.text(100))
        )

def popular_planos(cursor, quantidade):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO PlanoSaude (id_plano, nome_plano, codigo_operadora, tipo_cobertura) VALUES (%s, %s, %s, %s)",
            (i, fake.company(), fake.bothify(text='???-#####'), random.choice(['Ambulatorial', 'Hospitalar', 'Odontológico']))
        )

def popular_pacientes(cursor, quantidade):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO Paciente (id_paciente, nome, cpf, data_nascimento, sexo, endereco, email) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (i, fake.name(), fake.cpf(), fake.date_of_birth(minimum_age=0, maximum_age=90), random.choice(['Masculino', 'Feminino']), fake.address(), fake.email())
        )

def popular_salas(cursor, quantidade):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO Sala (id_sala, numero_sala, tipo_sala, andar) VALUES (%s, %s, %s, %s)",
            (i, random.randint(100, 999), random.choice(['Cirurgia', 'UTI', 'Consultório', 'Internação']), random.randint(1, 10))
        )

def popular_medicos(cursor, quantidade, max_departamentos):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO Medico (id_medico, nome_med, crm, especialidade, telefone, email, departamento_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (i, fake.name(), fake.bothify(text='CRM-#######'), fake.job(), fake.phone_number(), fake.email(), random.randint(1, max_departamentos))
        )

def popular_enfermeiros(cursor, quantidade):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO Enfermeiro (id_enfermeiro, nome_enfermeiro, registro_coren, turno, telefone, email) VALUES (%s, %s, %s, %s, %s, %s)",
            (i, fake.name(), fake.bothify(text='COREN-####'), random.choice(['Manhã', 'Tarde', 'Noite']), fake.phone_number(), fake.email())
        )

def popular_atendimentos(cursor, quantidade, max_pacientes, max_medicos, max_salas, max_enfermeiros, max_planos):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO Atendimento (id_atendimento, tipo_consulta, data_hora, paciente_id, medico_id, sala_id, enfermeiro_id, plano_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (i, random.choice(['Consulta', 'Emergência', 'Retorno']), fake.date_between(start_date='-1y', end_date='today'), 
             random.randint(1, max_pacientes), random.randint(1, max_medicos), random.randint(1, max_salas), random.randint(1, max_enfermeiros), random.randint(1, max_planos))
        )

def popular_exames(cursor, quantidade, max_pacientes, max_medicos, max_departamentos, max_salas, max_planos):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO Exame (id_exame, nome_exame, descricao, data_exame, resultado, paciente_id, medico_id, departamento_id, sala_id, plano_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (i, fake.word(), fake.text(100), fake.date_between(start_date='-1y', end_date='today'), fake.sentence(), 
             random.randint(1, max_pacientes), random.randint(1, max_medicos), random.randint(1, max_departamentos),
             random.randint(1, max_salas), random.randint(1, max_planos))
        )

def popular_medicamentos(cursor, quantidade):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO Medicamento (id_medicamento, nome_comercial, principio_ativo, formatacao, dosagem_padrao) VALUES (%s, %s, %s, %s, %s)",
            (i, fake.word().capitalize(), fake.word().capitalize(), random.choice(['Comprimido', 'Injetável', 'Pomada']), f"{random.randint(5, 500)}mg")
        )

def popular_prescricoes(cursor, quantidade, max_pacientes, max_medicos):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO Prescricao (id_prescricao, data_emissao, validade, instrucao, paciente_id, medico_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (i, fake.date_between(start_date='-30d', end_date='today'), f"{random.randint(5, 30)} dias", fake.text(80),
             random.randint(1, max_pacientes), random.randint(1, max_medicos))
        )

def popular_prescricao_medicamento(cursor, quantidade, max_prescricoes, max_medicamentos):
    for i in range(1, quantidade + 1):
        cursor.execute(
            "INSERT INTO Prescricao_Medicamento (id_prescricao_med, id_medicamento, id_prescricao) VALUES (%s, %s, %s)",
            (i, random.randint(1, max_medicamentos), random.randint(1, max_prescricoes))
        )


try:
    conn = conectar()
    if conn.is_connected():
        cursor = conn.cursor()

        qtd_departamentos = 5
        qtd_planos = 5
        qtd_pacientes = 100
        qtd_salas = 10
        qtd_medicos = 20
        qtd_enfermeiros = 20
        qtd_atendimentos = 150
        qtd_exames = 100
        qtd_medicamentos = 30
        qtd_prescricoes = 80
        qtd_prescricao_meds = 100

        popular_departamentos(cursor, qtd_departamentos)
        popular_planos(cursor, qtd_planos)
        popular_pacientes(cursor, qtd_pacientes)
        popular_salas(cursor, qtd_salas)
        popular_medicos(cursor, qtd_medicos, qtd_departamentos)
        popular_enfermeiros(cursor, qtd_enfermeiros)
        popular_atendimentos(cursor, qtd_atendimentos, qtd_pacientes, qtd_medicos, qtd_salas, qtd_enfermeiros, qtd_planos)
        popular_exames(cursor, qtd_exames, qtd_pacientes, qtd_medicos, qtd_departamentos, qtd_salas, qtd_planos)
        popular_medicamentos(cursor, qtd_medicamentos)
        popular_prescricoes(cursor, qtd_prescricoes, qtd_pacientes, qtd_medicos)
        popular_prescricao_medicamento(cursor, qtd_prescricao_meds, qtd_prescricoes, qtd_medicamentos)

        conn.commit()
        print("Dados inseridos com sucesso.")

except Error as e:
    print(f"Erro: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
