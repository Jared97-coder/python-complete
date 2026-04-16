"""
Módulo 10.3 - Mocking y Test Doubles

Técnicas de mocking con unittest.mock y pytest-mock:
- Mock objects
- Patch functions y métodos
- Side effects
- Spies y stubs
- MagicMock
- pytest-mock (mocker fixture)

Para ejecutar:
    pytest 03_mocking.py -v
    pytest 03_mocking.py -v -s  # Con stdout
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call, ANY
from datetime import datetime, timedelta
import requests  # Para ejemplos (instalar: pip install requests)

# =============================================================================
# CÓDIGO A TESTEAR
# =============================================================================

class EmailService:
    """Servicio de envío de emails (simulado)."""
    
    def send_email(self, to, subject, body):
        """Enviar email (interacción externa, ideal para mock)."""
        print(f"📧 Sending email to {to}: {subject}")
        # En producción: interacción con SMTP real
        return {"status": "sent", "to": to}
    
    def send_bulk_emails(self, recipients, subject, body):
        """Enviar emails masivos."""
        results = []
        for recipient in recipients:
            result = self.send_email(recipient, subject, body)
            results.append(result)
        return results


class UserService:
    """Servicio de usuarios."""
    
    def __init__(self, email_service):
        self.email_service = email_service
        self.users = {}
    
    def create_user(self, username, email):
        """Crear usuario y enviar email de bienvenida."""
        user_id = len(self.users) + 1
        self.users[user_id] = {'id': user_id, 'username': username, 'email': email}
        
        # Enviar email de bienvenida
        self.email_service.send_email(
            to=email,
            subject="Welcome!",
            body=f"Hello {username}, welcome to our platform!"
        )
        
        return user_id
    
    def get_user(self, user_id):
        """Obtener usuario."""
        return self.users.get(user_id)


class WeatherService:
    """Servicio que consume API externa."""
    
    def get_temperature(self, city):
        """Obtener temperatura (llamada API real)."""
        # En producción: requests.get("https://api.weather.com/...")
        response = requests.get(f"https://api.weather.com/city/{city}")
        data = response.json()
        return data['temperature']
    
    def is_sunny(self, city):
        """Verificar si hace sol."""
        response = requests.get(f"https://api.weather.com/city/{city}")
        data = response.json()
        return data['condition'] == 'sunny'


class PaymentProcessor:
    """Procesador de pagos (gateway externo)."""
    
    def charge(self, amount, card_number):
        """Procesar cargo (interacción externa)."""
        # En producción: Stripe, PayPal, etc.
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        print(f"💳 Charging ${amount} to card ending in {card_number[-4:]}")
        return {"transaction_id": "txn_123", "status": "approved"}


class OrderService:
    """Servicio de órdenes."""
    
    def __init__(self, payment_processor, email_service):
        self.payment_processor = payment_processor
        self.email_service = email_service
    
    def process_order(self, user_email, amount, card_number):
        """Procesar orden: Cobrar y enviar confirmación."""
        # Procesar pago
        payment_result = self.payment_processor.charge(amount, card_number)
        
        # Enviar confirmación
        if payment_result['status'] == 'approved':
            self.email_service.send_email(
                to=user_email,
                subject="Order Confirmation",
                body=f"Your order of ${amount} has been confirmed."
            )
            return {"success": True, "transaction_id": payment_result['transaction_id']}
        
        return {"success": False}


def get_current_user():
    """Obtener usuario actual (simulado)."""
    # En producción: query a database, session, etc.
    return {"id": 1, "username": "admin"}


# =============================================================================
# Ejemplo 1: Mock Básico
# =============================================================================

def test_mock_basic():
    """Test con Mock básico."""
    # Crear mock
    mock_email = Mock()
    
    # Configurar retorno
    mock_email.send_email.return_value = {"status": "sent"}
    
    # Usar mock
    result = mock_email.send_email("test@example.com", "Subject", "Body")
    
    # Verificar
    assert result == {"status": "sent"}
    
    # Verificar que fue llamado
    mock_email.send_email.assert_called_once()
    
    # Verificar argumentos
    mock_email.send_email.assert_called_once_with(
        "test@example.com", "Subject", "Body"
    )


print("=== Ejemplo 1: Mock Básico ===")
print("Mock(): Crear objeto mock simple\n")


# =============================================================================
# Ejemplo 2: Mock como Dependency Injection
# =============================================================================

def test_user_service_with_mock():
    """Test de UserService usando mock de EmailService."""
    # Crear mock de dependencia
    mock_email_service = Mock(spec=EmailService)
    
    # Crear servicio con mock inyectado
    user_service = UserService(email_service=mock_email_service)
    
    # Ejecutar
    user_id = user_service.create_user("alice", "alice@example.com")
    
    # Verificar
    assert user_id == 1
    assert user_service.get_user(user_id)["username"] == "alice"
    
    # Verificar que se envió email
    mock_email_service.send_email.assert_called_once_with(
        to="alice@example.com",
        subject="Welcome!",
        body="Hello alice, welcome to our platform!"
    )


print("=== Ejemplo 2: Mock como Dependency Injection ===")
print("Inyectar mocks en lugar de dependencias reales\n")


# =============================================================================
# Ejemplo 3: Patch de Funciones
# =============================================================================

@patch('requests.get')
def test_weather_service_with_patch(mock_get):
    """Test usando patch para mockear requests.get."""
    # Configurar mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        'temperature': 25,
        'condition': 'sunny'
    }
    mock_get.return_value = mock_response
    
    # Ejecutar código que usa requests.get
    weather_service = WeatherService()
    temp = weather_service.get_temperature("London")
    
    # Verificar
    assert temp == 25
    
    # Verificar que requests.get fue llamado
    mock_get.assert_called_once_with("https://api.weather.com/city/London")


print("=== Ejemplo 3: Patch de Funciones ===")
print("@patch('module.function'): Reemplazar función temporalmente\n")


# =============================================================================
# Ejemplo 4: Patch como Context Manager
# =============================================================================

def test_weather_with_context_manager():
    """Test usando patch como context manager."""
    with patch('requests.get') as mock_get:
        # Configurar mock
        mock_get.return_value.json.return_value = {
            'temperature': 30,
            'condition': 'sunny'
        }
        
        # Ejecutar
        weather_service = WeatherService()
        is_sunny = weather_service.is_sunny("Madrid")
        
        # Verificar
        assert is_sunny is True


print("=== Ejemplo 4: Patch como Context Manager ===")
print("with patch(...): Scope limitado al with block\n")


# =============================================================================
# Ejemplo 5: Patch de Métodos de Clase
# =============================================================================

@patch.object(EmailService, 'send_email')
def test_patch_object(mock_send_email):
    """Test usando patch.object para métodos de clase."""
    # Configurar mock
    mock_send_email.return_value = {"status": "sent"}
    
    # Crear instancia real (pero send_email está mockeado)
    email_service = EmailService()
    result = email_service.send_email("test@example.com", "Subject", "Body")
    
    # Verificar
    assert result == {"status": "sent"}
    mock_send_email.assert_called_once()


print("=== Ejemplo 5: Patch de Métodos ===")
print("@patch.object(Class, 'method'): Mockear método específico\n")


# =============================================================================
# Ejemplo 6: Multiple Patches
# =============================================================================

@patch

.object(EmailService, 'send_email')
@patch.object(PaymentProcessor, 'charge')
def test_multiple_patches(mock_charge, mock_send_email):
    """
    Test con múltiples patches.
    
    Nota: Orden de parámetros es INVERSO al de decoradores.
    """
    # Configurar mocks
    mock_charge.return_value = {"transaction_id": "txn_123", "status": "approved"}
    mock_send_email.return_value = {"status": "sent"}
    
    # Ejecutar
    payment = PaymentProcessor()
    email = EmailService()
    order_service = OrderService(payment, email)
    
    result = order_service.process_order("user@example.com", 100.0, "4111111111111111")
    
    # Verificar
    assert result["success"] is True
    assert result["transaction_id"] == "txn_123"
    
    # Verificar llamadas
    mock_charge.assert_called_once_with(100.0, "4111111111111111")
    mock_send_email.assert_called_once()


print("=== Ejemplo 6: Multiple Patches ===")
print("Apilar decoradores @patch (orden inverso en parámetros)\n")


# =============================================================================
# Ejemplo 7: Side Effects
# =============================================================================

def test_side_effect_exception():
    """Test con side_effect para simular excepción."""
    mock_payment = Mock()
    mock_payment.charge.side_effect = ConnectionError("Payment gateway down")
    
    # Verificar que levanta excepción
    with pytest.raises(ConnectionError, match="Payment gateway down"):
        mock_payment.charge(100, "4111111111111111")


def test_side_effect_multiple_returns():
    """Test con side_effect para retornar valores diferentes."""
    mock_api = Mock()
    mock_api.fetch.side_effect = [
        {"data": "first"},
        {"data": "second"},
        {"data": "third"}
    ]
    
    # Primera llamada
    assert mock_api.fetch() == {"data": "first"}
    
    # Segunda llamada
    assert mock_api.fetch() == {"data": "second"}
    
    # Tercera llamada
    assert mock_api.fetch() == {"data": "third"}


def test_side_effect_function():
    """Test con side_effect como función."""
    def custom_behavior(amount, card):
        if amount > 1000:
            raise ValueError("Amount too large")
        return {"status": "approved"}
    
    mock_payment = Mock()
    mock_payment.charge.side_effect = custom_behavior
    
    # Llamada normal
    result = mock_payment.charge(100, "4111111111111111")
    assert result["status"] == "approved"
    
    # Llamada que levanta excepción
    with pytest.raises(ValueError, match="Amount too large"):
        mock_payment.charge(2000, "4111111111111111")


print("=== Ejemplo 7: Side Effects ===")
print("side_effect: Excepciones, múltiples valores, o funciones\n")


# =============================================================================
# Ejemplo 8: Verificación de Llamadas
# =============================================================================

def test_mock_call_verification():
    """Test de verificación de llamadas a mock."""
    mock_email = Mock()
    
    # Llamar varias veces
    mock_email.send("alice@example.com", "Subject 1")
    mock_email.send("bob@example.com", "Subject 2")
    mock_email.send("charlie@example.com", "Subject 3")
    
    # Verificar número de llamadas
    assert mock_email.send.call_count == 3
    
    # Verificar que fue llamado (al menos una vez)
    mock_email.send.assert_called()
    
    # Verificar última llamada
    mock_email.send.assert_called_with("charlie@example.com", "Subject 3")
    
    # Verificar cualquier llamada (assert_any_call)
    mock_email.send.assert_any_call("alice@example.com", "Subject 1")
    
    # Verificar todas las llamadas
    expected_calls = [
        call("alice@example.com", "Subject 1"),
        call("bob@example.com", "Subject 2"),
        call("charlie@example.com", "Subject 3")
    ]
    mock_email.send.assert_has_calls(expected_calls)


print("=== Ejemplo 8: Verificación de Llamadas ===")
print("assert_called(), assert_called_once(), assert_has_calls()\n")


# =============================================================================
# Ejemplo 9: MagicMock
# =============================================================================

def test_magic_mock():
    """Test con MagicMock (soporta métodos mágicos)."""
    mock_list = MagicMock()
    
    # Configurar métodos mágicos
    mock_list.__len__.return_value = 3
    mock_list.__iter__.return_value = iter([1, 2, 3])
    mock_list.__getitem__.side_effect = lambda i: i * 10
    
    # Usar como lista
    assert len(mock_list) == 3
    assert list(mock_list) == [1, 2, 3]
    assert mock_list[5] == 50


def test_magic_mock_context_manager():
    """Test de MagicMock como context manager."""
    mock_file = MagicMock()
    mock_file.__enter__.return_value = mock_file
    mock_file.read.return_value = "file content"
    
    # Usar como context manager
    with mock_file as f:
        content = f.read()
        assert content == "file content"
    
    # Verificar que __enter__ y __exit__ fueron llamados
    mock_file.__enter__.assert_called_once()
    mock_file.__exit__.assert_called_once()


print("=== Ejemplo 9: MagicMock ===")
print("MagicMock: Mock con soporte para métodos mágicos (__len__, __iter__, etc.)\n")


# =============================================================================
# Ejemplo 10: Spec y Spec_set
# =============================================================================

def test_mock_with_spec():
    """Test con spec para restringir mock a interfaz real."""
    # Mock con spec: solo permite métodos que existan en EmailService
    mock_email = Mock(spec=EmailService)
    
    # Esto funciona (send_email existe)
    mock_email.send_email("test@example.com", "Subject", "Body")
    
    # Esto falla (método no existe en EmailService)
    with pytest.raises(AttributeError):
        mock_email.non_existent_method()


def test_mock_with_spec_set():
    """Test con spec_set (más estricto que spec)."""
    mock_email = Mock(spec_set=EmailService)
    
    # No se puede agregar atributos que no existan
    with pytest.raises(AttributeError):
        mock_email.new_attribute = "value"


print("=== Ejemplo 10: Spec y Spec_set ===")
print("spec: Restringir mock a interfaz real\n")


# =============================================================================
# Ejemplo 11: pytest-mock (mocker fixture)
# =============================================================================

def test_with_mocker(mocker):
    """
    Test usando mocker fixture de pytest-mock.
    
    Ventajas sobre unittest.mock:
    - Cleanup automático
    - Sintaxis más pythin
    - Integración con fixtures
    """
    # mocker.patch automáticamente hace cleanup
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {
        'temperature': 20,
        'condition': 'cloudy'
    }
    
    weather_service = WeatherService()
    temp = weather_service.get_temperature("Paris")
    
    assert temp == 20


def test_mocker_spy(mocker):
    """Test usando spy (wrapper que registra llamadas)."""
    email_service = EmailService()
    
    # Spy: Llama al método real pero registra llamadas
    spy = mocker.spy(email_service, 'send_email')
    
    # Llamar método real
    email_service.send_email("test@example.com", "Subject", "Body")
    
    # Verificar que fue llamado
    spy.assert_called_once_with("test@example.com", "Subject", "Body")


def test_mocker_stub(mocker):
    """Test usando stub (retorno configurable)."""
    # Stub: Mock simple con return_value
    stub = mocker.stub(name='payment_stub')
    stub.return_value = {"status": "approved"}
    
    result = stub()
    assert result == {"status": "approved"}


print("=== Ejemplo 11: pytest-mock ===")
print("mocker fixture: Alternativa pytest-friendly a unittest.mock\n")


# =============================================================================
# Ejemplo 12: Mock de datetime
# =============================================================================

@patch('03_mocking.datetime')
def test_mock_datetime(mock_datetime):
    """Test mockeando datetime.now()."""
    # Configurar fecha fija
    fake_now = datetime(2024, 1, 15, 12, 0, 0)
    mock_datetime.now.return_value = fake_now
    
    # Código que usa datetime.now()
    from datetime import datetime as dt
    # En producción usaría: current_time = datetime.now()
    current_time = mock_datetime.now()
    
    assert current_time == fake_now
    assert current_time.year == 2024


print("=== Ejemplo 12: Mock de datetime ===")
print("Útil para testear funcionalidad dependiente del tiempo\n")


# =============================================================================
# Ejemplo 13: Mock de Open (archivos)
# =============================================================================

def read_config_file(filename):
    """Leer archivo de configuración."""
    with open(filename, 'r') as f:
        return f.read()


def test_mock_open():
    """Test mockeando open()."""
    from unittest.mock import mock_open
    
    # Simular contenido de archivo
    fake_content = "setting1=value1\nsetting2=value2"
    
    with patch('builtins.open', mock_open(read_data=fake_content)):
        content = read_config_file('config.txt')
        
        assert content == fake_content
        assert "setting1=value1" in content


print("=== Ejemplo 13: Mock de Open ===")
print("mock_open(): Simular lectura/escritura de archivos\n")


# =============================================================================
# Ejemplo 14: ANY Matcher
# =============================================================================

def test_any_matcher():
    """Test usando ANY para verificar llamadas parciales."""
    from unittest.mock import ANY
    
    mock_email = Mock()
    mock_email.send("alice@example.com", "Subject", timestamp=datetime.now())
    
    # Verificar sin importar el timestamp exacto
    mock_email.send.assert_called_once_with(
        "alice@example.com",
        "Subject",
        timestamp=ANY  # Acepta cualquier valor
    )


print("=== Ejemplo 14: ANY Matcher ===")
print("ANY: Ignorar argumento específico en verificación\n")


# =============================================================================
# Ejemplo 15: Reset Mock
# =============================================================================

def test_reset_mock():
    """Test reseteando mock entre llamadas."""
    mock_api = Mock()
    
    # Primera serie de llamadas
    mock_api.fetch()
    mock_api.fetch()
    assert mock_api.fetch.call_count == 2
    
    # Reset
    mock_api.reset_mock()
    
    # Después de reset, contador en 0
    assert mock_api.fetch.call_count == 0
    
    # Nueva llamada
    mock_api.fetch()
    assert mock_api.fetch.call_count == 1


print("=== Ejemplo 15: Reset Mock ===")
print("reset_mock(): Limpiar historial de llamadas\n")


# =============================================================================
# INSTRUCCIONES DE EJECUCIÓN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("MOCKING Y TEST DOUBLES - MÓDULO 10.3")
    print("=" * 70)
    print("\nComandos de ejecución:")
    print("\n1. Ejecutar todos los tests:")
    print("   pytest 03_mocking.py -v")
    print("\n2. Con output (para ver prints):")
    print("   pytest 03_mocking.py -v -s")
    print("\n3. Ejecutar tests de patch:")
    print("   pytest 03_mocking.py -k 'patch' -v")
    print("\n4. Ejecutar tests de pytest-mock:")
    print("   pytest 03_mocking.py -k 'mocker' -v")
    print("\n" + "=" * 70)
    print("Conceptos cubiertos:")
    print("  ✓ Mock y MagicMock")
    print("  ✓ Patch de funciones y métodos")
    print("  ✓ Side effects")
    print("  ✓ Verificación de llamadas")
    print("  ✓ Spec y spec_set")
    print("  ✓ pytest-mock (mocker fixture)")
    print("  ✓ Mock de datetime, open, requests")
    print("  ✓ ANY matcher")
    print("=" * 70 + "\n")
