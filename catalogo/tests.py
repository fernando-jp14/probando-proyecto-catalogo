from django.test import TestCase, Client
from django.urls import reverse
from .models import Curso
from .forms import CursoForm

# 🧱 TESTS DEL MODELO CURSO
class CursoModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n🔷 INICIANDO TESTS DEL MODELO Curso")

    def test_creacion_curso_exitosa(self):
        print("🧪 Test: creación de curso válida")
        curso = Curso.objects.create(
            curso='Python Básico',
            duracion='10 horas',
            plataforma='Platzi',
            dificultad='Básico'
        )
        self.assertEqual(curso.curso, 'Python Básico')
        print("✅ Curso creado exitosamente")

    def test_str_del_modelo(self):
        print("🧪 Test: representación string del modelo")
        curso = Curso(curso='Django Intermedio')
        self.assertEqual(str(curso), 'Django Intermedio')
        print("✅ __str__ devuelve el nombre correctamente")

    def test_dificultad_valida(self):
        print("🧪 Test: dificultad pertenece a opciones válidas")
        curso = Curso(dificultad='Intermedio')
        self.assertIn(curso.dificultad, [op[0] for op in Curso.DIFICULTAD_OPCIONES])
        print("✅ Dificultad válida confirmada")


# 📋 TESTS DEL FORMULARIO
class CursoFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n🔷 INICIANDO TESTS DEL FORMULARIO CursoForm")

    def test_formulario_valido(self):
        print("🧪 Test: formulario con datos válidos")
        form = CursoForm(data={
            'curso': 'Backend con Django',
            'duracion': '15 horas',
            'plataforma': 'Udemy',
            'dificultad': 'Avanzado'
        })
        self.assertTrue(form.is_valid())
        print("✅ Formulario validado correctamente")

    def test_error_nombre_corto(self):
        print("🧪 Test: error por nombre de curso corto")
        form = CursoForm(data={
            'curso': 'Py',
            'duracion': '8h',
            'plataforma': 'Platzi',
            'dificultad': 'Básico'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('El nombre del curso debe tener al menos 3 caracteres.', form.errors['curso'])
        print("✅ Error personalizado detectado correctamente")

    def test_error_duracion_vacia(self):
        print("🧪 Test: error por duración vacía")
        form = CursoForm(data={
            'curso': 'JavaScript',
            'duracion': '',
            'plataforma': 'Platzi',
            'dificultad': 'Básico'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('La duración es obligatoria.', form.errors['duracion'])
        print("✅ Validación de duración ejecutada correctamente")

    def test_error_plataforma_vacia(self):
        print("🧪 Test: error por plataforma vacía")
        form = CursoForm(data={
            'curso': 'CSS Master',
            'duracion': '6h',
            'plataforma': '',
            'dificultad': 'Intermedio'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('La plataforma es obligatoria.', form.errors['plataforma'])
        print("✅ Validación de plataforma ejecutada correctamente")


# 🌐 TESTS DE VISTAS
class CursoViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n🔷 INICIANDO TESTS DE LAS VISTAS")

    def setUp(self):
        self.client = Client()
        self.curso = Curso.objects.create(
            curso='Prueba',
            duracion='2 horas',
            plataforma='YouTube',
            dificultad='Básico'
        )

    def test_lista_cursos_status(self):
        print("🧪 Test: vista de lista de cursos")
        response = self.client.get(reverse('lista_cursos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogo/lista_cursos.html')
        print("✅ Vista de lista cargada correctamente")

    def test_crear_curso_post_valido(self):
        print("🧪 Test: crear curso vía POST")
        response = self.client.post(reverse('crear_curso'), {
            'curso': 'Nuevo Curso',
            'duracion': '5h',
            'plataforma': 'Platzi',
            'dificultad': 'Intermedio'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Curso.objects.count(), 2)
        print("✅ Curso creado y redirección exitosa")

    def test_editar_curso_post(self):
        print("🧪 Test: editar curso existente")
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

    def test_eliminar_curso(self):
        print("🧪 Test: eliminar curso por vista")
        response = self.client.get(reverse('eliminar_curso', args=[self.curso.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Curso.objects.count(), 0)
        print("✅ Curso eliminado y redirigido correctamente")


# 🛣️ TESTS DE URLS
class CursoUrlsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("\n🔷 INICIANDO TESTS DE LAS URLS")

    def test_urls_existentes(self):
        print("🧪 Test: rutas configuradas correctamente")
        self.assertEqual(reverse('lista_cursos'), '/')
        self.assertEqual(reverse('crear_curso'), '/crear/')
        self.assertEqual(reverse('editar_curso', args=[1]), '/editar/1/')
        self.assertEqual(reverse('eliminar_curso', args=[1]), '/eliminar/1/')
        print("✅ Rutas Django están funcionando bien")