import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {

    static String dataApiUrl = System.getenv("MONGO_DATA_API_URL");
    static String dataApiKey = System.getenv("MONGO_DATA_API_KEY");
    static String dataSource = System.getenv("MONGO_DATA_SOURCE");
    static String database = System.getenv("MONGO_DATABASE");
    static String collection = System.getenv("MONGO_COLLECTION");

    public static void main(String[] args) throws IOException {
        int puerto = Integer.parseInt(System.getenv().getOrDefault("PORT", "8080"));
        HttpServer servidor = HttpServer.create(new InetSocketAddress(puerto), 0);

        servidor.createContext("/", exchange -> {
            if (exchange.getRequestURI().getPath().equals("/") && exchange.getRequestMethod().equals("GET")) {
                responderJson(exchange, 200, "{\"mensaje\":\"Microservicio de eliminacion de consejos (Java) funcionando\"}");
                return;
            }
            responderJson(exchange, 404, "{\"error\":\"Ruta no encontrada\"}");
        });

        servidor.createContext("/api-docs", exchange -> {
            String html = "<!DOCTYPE html>"
                    + "<html lang=\"es\"><head><meta charset=\"UTF-8\">"
                    + "<title>Microservicio de Eliminación de Mascotas</title>"
                    + "<link rel=\"stylesheet\" href=\"https://unpkg.com/swagger-ui-dist@5/swagger-ui.css\" />"
                    + "</head><body><div id=\"swagger-ui\"></div>"
                    + "<script src=\"https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js\"></script>"
                    + "<script>window.onload = () => {"
                    + "SwaggerUIBundle({"
                    + "  dom_id: '#swagger-ui',"
                    + "  spec: {"
                    + "    openapi: '3.0.0',"
                    + "    info: { title: 'Microservicio de Eliminación de Mascotas', version: '1.0.0', description: 'Microservicio en Java para eliminar registros de mascotas.' },"
                    + "    servers: [{ url: 'https://microservicio-eliminar-java.onrender.com', description: 'Servidor de Producción' }],"
                    + "    paths: {"
                    + "      '/': { get: { summary: 'Verificar estado del microservicio', responses: { '200': { description: 'Servicio activo' } } } },"
                    + "      '/eliminar': {"
                    + "        delete: {"
                    + "          summary: 'Eliminar una mascota por ID',"
                    + "          requestBody: { required: true, content: { 'application/json': { schema: { type: 'object', properties: { id: { type: 'string' } } } } } },"
                    + "          responses: { '200': { description: 'Registro eliminado correctamente' } }"
                    + "        }"
                    + "      }"
                    + "    }"
                    + "  }"
                    + "});"
                    + "};</script></body></html>";

            exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
            byte[] bytes = html.getBytes(StandardCharsets.UTF_8);
            exchange.sendResponseHeaders(200, bytes.length);
            OutputStream salida = exchange.getResponseBody();
            salida.write(bytes);
            salida.close();
        });

        servidor.createContext("/eliminar", exchange -> {
            if (!exchange.getRequestMethod().equals("DELETE")) {
                responderJson(exchange, 405, "{\"error\":\"Metodo no permitido\"}");
                return;
            }

            String cuerpo = leerCuerpo(exchange.getRequestBody());
            String id = extraerCampo(cuerpo, "id");

            if (id == null) {
                responderJson(exchange, 400, "{\"error\":\"Se necesita el campo id\"}");
                return;
            }

            try {
                String resultado = eliminarEnMongo(id);
                if (resultado.contains("\"deletedCount\":1")) {
                    responderJson(exchange, 200, "{\"mensaje\":\"Consejo eliminado correctamente\"}");
                } else {
                    responderJson(exchange, 404, "{\"error\":\"No se encontro un consejo con ese id\"}");
                }
            } catch (Exception e) {
                responderJson(exchange, 500, "{\"error\":\"No se pudo eliminar\"}");
            }
        });

        servidor.start();
        System.out.println("Servidor corriendo en el puerto " + puerto);
    }

    static String eliminarEnMongo(String id) throws Exception {
        String cuerpoJson = "{"
                + "\"dataSource\":\"" + dataSource + "\","
                + "\"database\":\"" + database + "\","
                + "\"collection\":\"" + collection + "\","
                + "\"filter\":{\"_id\":{\"$oid\":\"" + id + "\"}}"
                + "}";

        HttpClient cliente = HttpClient.newHttpClient();
        HttpRequest peticion = HttpRequest.newBuilder()
                .uri(URI.create(dataApiUrl + "/action/deleteOne"))
                .header("Content-Type", "application/json")
                .header("api-key", dataApiKey)
                .POST(HttpRequest.BodyPublishers.ofString(cuerpoJson))
                .build();

        HttpResponse<String> respuesta = cliente.send(peticion, HttpResponse.BodyHandlers.ofString());
        return respuesta.body();
    }

    static String leerCuerpo(InputStream entrada) throws IOException {
        return new String(entrada.readAllBytes(), StandardCharsets.UTF_8);
    }

    static String extraerCampo(String json, String campo) {
        Pattern patron = Pattern.compile("\"" + campo + "\"\\s*:\\s*\"([^\"]*)\"");
        Matcher coincidencia = patron.matcher(json);
        if (coincidencia.find()) {
            return coincidencia.group(1);
        }
        return null;
    }

    static void responderJson(HttpExchange exchange, int codigo, String cuerpo) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        byte[] bytes = cuerpo.getBytes(StandardCharsets.UTF_8);
        exchange.sendResponseHeaders(codigo, bytes.length);
        OutputStream salida = exchange.getResponseBody();
        salida.write(bytes);
        salida.close();
    }
}