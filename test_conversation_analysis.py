#!/usr/bin/env python3
"""
🧪 Test script para análisis de conversaciones con Watson
"""

import requests
import json

# Conversación real de ejemplo de la base de datos
SAMPLE_CONVERSATION = """Operador: Sí, muy buenas noches, caballero. Me comunico por parte de soporte técnico. Hace un momento lo llamé, pero me comentó que la llamada se cortó hace media hora. Lo llamo con el motivo de que está experimentando lentitud en su servicio. Le comento que antes de esta llamada, un compañero estuvo realizando varios ajustes en su servicio. Él me informó que el servicio se encuentra un poquito más estable. Yo también estoy revisando y estoy viendo parámetros más correctos, pero me comunico con usted para validar que pruebe el servicio para ver si aún percibe la lentitud. En caso de que sea así, veremos qué otro ajuste podemos realizar.
Cliente: A ver, más o menos... ¿mi internet está muy lento? Yo he tenido por mucho tiempo este internet y los mismos megas y funcionaba bien. Teníamos varios aparatos conectados a la vez. Después salimos de la casa y le dejamos de pagar, y volvimos a hacer un contrato. Pero esta vez sí está muy lento. Hay una luz naranja que me indica que la red es baja. Es por eso que puse el reporte. No entendí muy bien lo que me dijiste. ¿Ustedes allá lo van a intentar componer o va a venir un técnico a arreglarlo?
Operador: Con gusto, nuevamente le repito. Le estaba comentando que nos llegó el reporte de lentitud este mismo día. Pero, antes de que yo lo llamara, un compañero estuvo ajustando su servicio para ese mismo tema. Ahorita yo también estuve revisando su servicio para verificar que estuviera funcionando y veo parámetros un poquito más correctos. Le estoy marcando para que pruebe su servicio con los ajustes que mi compañero realizó hace unas horas y así veamos si ya funciona de manera correcta y si ya no percibe la lentitud.
Cliente: Okay, muy bien, ahora sí ya te entendí. Mira, ahorita yo no estoy en mi casa. Estaba trabajando, por eso no podía contestar. Yo creo que en un rato más, en una media hora, llego a mi casa y reviso la situación. En caso de que el problema prevalezca, se los hago saber. Y si ya está corregido, también se los hago saber.
Operador: Okay, caballero. Entonces, ¿le devuelvo la llamada en media hora, o usted estará probando el servicio esta noche?
Cliente: Sí, mejor... sí, mira. No sé hasta qué hora puedas marcarme.
Operador: No se preocupe. Nosotros tenemos atención hasta las diez de la noche.
Cliente: Me parece bien, a las nueve está bien.
Operador: Okay, a las nueve de la noche desea que le devolvamos la llamada.
Cliente: Sí, por favor.
Operador: Okay, claro. Le pasaré el reporte para que le devuelva la llamada más tarde. En caso de que no lo contacte hoy, se la devolvería mañana temprano.
Cliente: Muy bien, muchas gracias.
Operador: Okay, queda. Que tenga una excelente noche.
Cliente: Gracias, igualmente."""

BASE_URL = "http://localhost:8001/api/v1"

def test_conversation_analysis():
    """Test análisis de conversación con datos reales"""
    print("🧠 Testing conversation analysis...")
    
    payload = {
        "conversation": SAMPLE_CONVERSATION,
        "operator_id": 1,
        "client_ref": "CLI-001",
        "call_date": "2025-03-03",
        "call_label": "llamada 1"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/watson/analyze-conversation",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Conversación analizada exitosamente!")
            print(f"📋 Call ID: {result['call_id']}")
            
            analysis = result['analysis']
            print("\n🔍 ANÁLISIS DETALLADO:")
            print("=" * 50)
            
            # Análisis de la llamada
            call_analysis = analysis['call_analysis']
            print(f"🎯 Tipo de problema: {call_analysis['problem_type']}")
            print(f"⚡ Nivel de urgencia: {call_analysis['urgency_level']}")
            print(f"😊 Sentimiento cliente: {call_analysis['customer_sentiment']}")
            print(f"📊 Estado resolución: {call_analysis['resolution_status']}")
            print(f"📞 Requiere seguimiento: {'Sí' if call_analysis['follow_up_required'] else 'No'}")
            
            # Entidades extraídas
            entities = analysis['extracted_entities']
            print(f"\n📋 ENTIDADES EXTRAÍDAS:")
            for key, value in entities.items():
                if value is not None:
                    print(f"• {key}: {value}")
            
            # Recomendaciones
            recommendations = analysis['recommended_actions']
            print(f"\n💡 RECOMENDACIONES:")
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
            
            # Resumen
            print(f"\n📝 RESUMEN:")
            print(analysis['summary'])
            
            return True
            
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_watson_intelligence():
    """Simular cómo Watson usaría el análisis"""
    print("\n🤖 SIMULACIÓN: Watson analizando conversación...")
    print("=" * 60)
    
    # Simular que Watson envía la conversación para análisis
    print("👨‍💼 Operador termina llamada con cliente")
    print("📞 Sistema registra conversación en base de datos")
    print("🤖 Watson detecta nueva conversación")
    print("🧠 Watson envía conversación para análisis automático...")
    
    # Ejecutar análisis
    success = test_conversation_analysis()
    
    if success:
        print("\n🎯 ACCIONES QUE WATSON PODRÍA TOMAR:")
        print("1. 🎫 Crear ticket automático: 'Lentitud servicio - Cliente CLI-001'")
        print("2. 📅 Programar callback automático para las 21:00")
        print("3. 📧 Enviar notificación a técnicos: 'Ajustes realizados, verificar efectividad'")
        print("4. 📊 Actualizar dashboard con estado de resolución")
        print("5. 🔔 Alertar supervisor sobre callback programado")
        
        print("\n💬 RESPUESTA DE WATSON AL OPERADOR:")
        print("'✅ Conversación analizada. He detectado:")
        print("• Problema: Lentitud de servicio")
        print("• Ajustes ya realizados por compañero")
        print("• Callback programado: 21:00")
        print("• Estado: Pendiente verificación cliente")
        print("¿Quieres que cree un ticket de seguimiento?'")

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 UANL Watson Conversation Analysis Test")
    print("=" * 60)
    
    # Test básico
    success = test_conversation_analysis()
    
    if success:
        # Simulación de inteligencia Watson
        test_watson_intelligence()
        
        print("\n🎉 ¡Sistema de análisis de conversaciones listo!")
        print("Watson ahora puede:")
        print("✅ Analizar conversaciones automáticamente")
        print("✅ Extraer entidades y sentimientos")
        print("✅ Generar recomendaciones inteligentes")
        print("✅ Crear resúmenes automáticos")
        print("✅ Detectar necesidad de seguimiento")
    else:
        print("\n❌ Error en el análisis. Verificar servidor.")

if __name__ == "__main__":
    main()
