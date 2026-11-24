"""Pruebas automáticas. Funcionan con pytest (`pytest`) o sin él (`python tests/test_sbc.py`)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from base_conocimiento import REGLAS, PREDICADOS                       # noqa: E402
from motor_inferencia import (validar_base, diagnosticar, encadenamiento_adelante,   # noqa: E402
                              validar_entrada, porque, clasificar_resultado)
from casos_prueba import ejecutar_casos                                  # noqa: E402
from validacion import cobertura_por_regla, explorar_escenarios, validar_catalogo_completo   # noqa: E402
from catalogo_modelos import (MODELOS, imagen_svg, sintoma_aplica, bloqueos_del_modelo,   # noqa: E402
                              hechos_del_modelo, modelos_de_marca)
from base_conocimiento import MARCAS                                      # noqa: E402


def test_base_consistente():
    assert validar_base(REGLAS) == []


def test_casos_de_prueba():
    fallos = [r for r in ejecutar_casos() if not r["ok"]]
    assert fallos == [], fallos


def test_cada_regla_se_dispara():
    assert cobertura_por_regla() == []


def test_exploracion_sistematica():
    resultado = explorar_escenarios()
    assert resultado["total"] > 50000
    assert resultado["violaciones"] == []


def test_sin_conclusion():
    hechos, aplicadas = diagnosticar({"luces_debiles"})
    assert aplicadas == []


def test_entrada_invalida():
    assert validar_entrada(set())
    assert validar_entrada({"marcha_gira", "marcha_no_gira"})
    assert validar_entrada({"tirones"}, "marca_inexistente")


def test_porque_reconstruye_la_cadena():
    sintomas = {"marcha_gira", "sin_chispa", "bujia_sucia"}
    hechos, aplicadas = diagnosticar(sintomas)
    texto = porque("recomendar_bujia_danada", sintomas, aplicadas)
    assert "falla_encendido" in texto and "marcha_gira" in texto


def test_marca_solo_activa_sus_reglas():
    _, ap_ktm = diagnosticar({"bateria_se_descarga", "luces_debiles_en_marcha"}, "ktm")
    _, ap_sin = diagnosticar({"bateria_se_descarga", "luces_debiles_en_marcha"})
    assert "regulador_rectificador_ktm" in {a["entonces"] for a in ap_ktm}
    assert "regulador_rectificador_ktm" not in {a["entonces"] for a in ap_sin}


def test_deteccion_de_ciclos_en_la_base():
    ciclica = [{"nombre": "A", "descripcion": "", "si": ["x"], "entonces": "y", "certeza": 1.0},
               {"nombre": "B", "descripcion": "", "si": ["y"], "entonces": "x", "certeza": 1.0}]
    assert any("Ciclo" in p for p in validar_base(ciclica))


def test_clasificar_resultado():
    _, ap = diagnosticar({"freno_esponjoso", "nivel_liquido_bajo"})
    grupos = clasificar_resultado(ap)
    assert grupos["alertas"] and grupos["diagnosticos"] and grupos["recomendaciones"]


def test_catalogo_consistente():
    assert validar_catalogo_completo() == []
    assert len(MODELOS) >= 40
    for marca in MARCAS:
        assert len(modelos_de_marca(marca)) >= 3, marca


def test_imagenes_svg_bien_formadas():
    from xml.etree import ElementTree
    for mid in MODELOS:
        ElementTree.fromstring(imagen_svg(mid))


def test_modelo_oculta_sintomas_que_no_aplican():
    assert not sintoma_aplica("ruido_cadena", "yamaha_nmax_155")        # scooter CVT: sin cadena
    assert sintoma_aplica("ruido_cadena", "yamaha_r15")
    assert not sintoma_aplica("nivel_refrigerante_bajo", "ducati_scrambler_800")   # enfriada por aire
    assert sintoma_aplica("ruido_cadena", "")                            # sin modelo todo aplica
    assert validar_entrada({"ruido_cadena"}, "", "yamaha_nmax_155")      # la validación lo rechaza


def test_modelo_bloquea_diagnosticos_incompatibles():
    assert "termostato_ventilador_kawasaki" in bloqueos_del_modelo("kawasaki_klx_230")
    _, ap = diagnosticar({"sobrecalentamiento", "falla_en_trafico_lento"}, "", "kawasaki_klx_230")
    derivados = {a["entonces"] for a in ap}
    assert "termostato_ventilador_kawasaki" not in derivados
    assert "calentamiento_motor_aire_trafico" in derivados


def test_modelo_implica_marca_y_aporta_hechos():
    hechos, _ = diagnosticar({"bateria_se_descarga", "luces_debiles_en_marcha"}, "", "ktm_390_duke")
    assert "marca_ktm" in hechos and "modelo_ktm_390_duke" in hechos and "regulador_rectificador_ktm" in hechos
    assert hechos_del_modelo("ktm_390_duke") <= hechos


def test_modelo_de_otra_marca_se_rechaza():
    assert validar_entrada({"tirones"}, "ducati", "ktm_390_duke")


if __name__ == "__main__":
    pruebas = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    fallos = 0
    for nombre, funcion in pruebas:
        try:
            funcion()
            print("✓", nombre)
        except AssertionError as e:
            fallos += 1
            print("✗", nombre, str(e)[:200])
    print(f"\n{len(pruebas) - fallos} de {len(pruebas)} pruebas aprobadas")
    sys.exit(1 if fallos else 0)
