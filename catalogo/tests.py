from django.test import TestCase, Client
from django.urls import reverse
from .models import Curso
from .forms import CursoForm

# 🧱 TESTS DEL MODELO Curso
class CursoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\n🔷 INICIANDO TESTS DEL MODELO Curso")

    def test_crea_curso_con_campos_validos(self):
        curso = Curso.objects.create(
            curso='Python Básico',
            duracion='10 horas',
            plataforma='Platzi',
            dificultad='Básico'
        )
        self.assertEqual(curso.curso, 'Python Básico')
        print("✅ Curso creado exitosamente")

    def test_str_modelo_devuelve_nombre(self):
        curso = Curso(curso='Django Intermedio')
        self.assertEqual(str(curso), 'Django Intermedio')
        print("✅ __str__ funciona correctamente")

    def test_dificultad_es_valida(self):
        curso = Curso(dificultad='Intermedio')
        self.assertIn(curso.dificultad, [op[0] for op in Curso.DIFICULTAD_OPCIONES])
        print("✅ Dificultad dentro de opciones válidas")


# 📋 TESTS DEL FORMULARIO CursoForm
class CursoFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\n🔷 INICIANDO TESTS DEL FORMULARIO CursoForm")

    def test_form_valido_con_datos_correctos(self):
        form_data = {
            'curso': 'Backend con Django',
            'duracion': '15 horas',
            'plataforma': 'Udemy',
            'dificultad': 'Avanzado'
        }
        form = CursoForm(data=form_data)
        self.assertTrue(form.is_valid())
        print("✅ Formulario válido con datos completos")

    def test_form_falla_por_nombre_corto(self):
        form_data = {
            'curso': 'Py',
            'duracion': '8h',
            'plataforma': 'Platzi',
            'dificultad': 'Básico'
        }
        form = CursoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('El nombre del curso debe tener al menos 3 caracteres.', form.errors['curso'])
        print("✅ Nombre corto detectado correctamente")

    def test_form_falla_por_duracion_vacia(self):
        form_data = {
            'curso': 'JavaScript',
            'duracion': '',
            'plataforma': 'Platzi',
            'dificultad': 'Básico'
        }
        form = CursoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('La duración es obligatoria.', form.errors['duracion'])
        print("✅ Duración vacía detectada correctamente")

    def test_form_falla_por_plataforma_vacia(self):
        form_data = {
            'curso': 'CSS Master',
            'duracion': '6h',
            'plataforma': '',
            'dificultad': 'Intermedio'
        }
        form = CursoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('La plataforma es obligatoria.', form.errors['plataforma'])
        print("✅ Plataforma vacía detectada correctamente")


# 🌐 TESTS DE VISTAS
class CursoViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\n🔷 INICIANDO TESTS DE LAS VISTAS")
        cls.curso = Curso.objects.create(
            curso='Prueba',
            duracion='2 horas',
            plataforma='YouTube',
            dificultad='Básico'
        )

    def setUp(self):
        self.client = Client()

    def test_lista_cursos_carga_template(self):
        response = self.client.get(reverse('lista_cursos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/lista_cursos.html')
        print("✅ Vista lista_cursos cargada correctamente")

    def test_crear_curso_redirige_correctamente(self):
        response = self.client.post(reverse('crear_curso'), {
            'curso': 'Nuevo Curso',
            'duracion': '5h',
            'plataforma': 'Platzi',
            'dificultad': 'Intermedio'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Curso.objects.count(), 2)
        print("✅ Curso creado y redirigido con éxito")

    def test_editar_actualiza_curso(self):
        response = self.client.post(reverse('editar_curso', args=[self.curso.id]), {
            'curso': 'Editado',
            'duracion': '3h',
            'plataforma': 'Udemy',
            'dificultad': 'Avanzado'
        })
        self.assertEqual(response.status_code, 302)
        self.curso.refresh_from_db()
        self.assertEqual(self.curso.curso, 'Editado')
        print("✅ Curso editado correctamente")

    def test_eliminar_quita_curso(self):
        response = self.client.get(reverse('eliminar_curso', args=[self.curso.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Curso.objects.count(), 0)
        print("✅ Curso eliminado correctamente")


# 🛣️ TESTS DE URLS
class CursoUrlsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\n🔷 INICIANDO TESTS DE LAS URLS")

    def test_rutas_existentes_resuelven_bien(self):
        self.assertEqual(reverse('lista_cursos'), '/')
        self.assertEqual(reverse('crear_curso'), '/crear/')
        self.assertEqual(reverse('editar_curso', args=[1]), '/editar/1/')
        self.assertEqual(reverse('eliminar_curso', args=[1]), '/eliminar/1/')
        print("✅ Todas las rutas están configuradas correctamente")
