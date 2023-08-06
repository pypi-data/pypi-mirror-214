# Orr-Sommerfeld-convmix-CGB
## Una herramienta numérica para el analisis de estabilidad lineal de flujos en convección mixta en canales rectangulares verticales 
### ¿En qué consiste Orr-Sommerfeld-convmix-CGB?
Orr-Sommerfeld-convmix-CGB, es una herramienta computacional que permite calcular las frecuencias y amplitudes de las perturbaciónes modales propuestas por la teoría de la estabilidad lineal, mediante esquemas espectrales de Chebysheb.
### Teoría de la estabilidad lineal
La **transición laminar-turbulenta** es crucial en ingeniería y física aplicada. El flujo de un fluido puede ser laminar (ordenado) o turbulento (caótico), con impacto en la transferencia de calor. La transición es relevante en reactores nucleares, intercambiadores de calor y más. Aunque no se comprende completamente, se estudia desde hace más de cien años. 
![Reactor de investigación RA-6, Centro Atómico Bariloche, Argentina](ruta_de_la_imagen)
![Texto alternativo](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/RA6cab.jpg/1200px-RA6cab.jpg)
La evolución del flujo, tanto en el tiempo como en el espacio depende de las perturbaciones externas que el mismo reciba, como cambios de presión, temperatura, y de las condiciones de borde a las que esé sometido, como la rugosidad y fuentes de calor en las paredes, gradiente de presion, etc. 
Para entender cuáles son las condiciones de flujo que pueden producir esta transición desde el punto de vista matemático, es decir cuáles son sus estados iniciales o desencadenantes y cómo la afecta la transferencia de calor, se puede utilizar la **teoría de estabilidad lineal**. Ésta, propone un modelo matemático para predecir cuándo un flujo laminar se volverá turbulento mediante el análisis de pequeñas perturbaciones  en un flujo laminar estable y determina si estas perturbaciones crecerán o  se amortiguarán en el espacio y en el tiempo. Si las perturbaciones crecen, el flujo laminar se volverá inestable y eventualmente se transitará a un flujo turbulento. Cabe resaltar que en el presente trabajo, será de interés estudiar la transición en el tiempo, tomando como inputs las variables espaciales.

