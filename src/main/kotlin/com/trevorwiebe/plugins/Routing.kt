package com.trevorwiebe.plugins

import com.trevorwiebe.domain.GetRainAmounts
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.coroutines.runBlocking
import java.io.File

fun Application.configureRouting() {
    routing {
        get("/tile/{utcTime}/{zoom_level}/{x}/{y}") {

            val utcTime = call.parameters["utcTime"] ?: return@get call.respondText(
                "Missing or malformed utc time",
                status = HttpStatusCode.BadRequest
            )

            val zoomLevel = call.parameters["zoom_level"] ?: return@get call.respondText(
                "Missing or malformed zoom_level",
                status = HttpStatusCode.BadRequest
            )
            val x = call.parameters["x"] ?: return@get call.respondText(
                "Missing or malformed x",
                status = HttpStatusCode.BadRequest
            )
            val y = call.parameters["y"] ?: return@get call.respondText(
                "Missing or malformed y",
                status = HttpStatusCode.BadRequest
            )

            val fileName = "/root/radar-processing-data/app_data/$utcTime/$zoomLevel/$x/$y.png"
            val imageFile = File(fileName)

            if (imageFile.exists()) {
                call.respondBytes(imageFile.readBytes(), contentType = ContentType.Image.PNG)
            } else {
                call.respondText("Image not found", status = HttpStatusCode.NotFound)
            }
        }

        get("/rain"){
            val latitude = call.request.queryParameters["lat"]?.toFloatOrNull()
            val longitude = call.request.queryParameters["lon"]?.toFloatOrNull()

            if(latitude == null || longitude == null){
                return@get call.respondText(
                    text = "latitude and longitude are both required",
                    status = HttpStatusCode.BadRequest
                )
            }

            GetRainAmounts().invoke(latitude.toString(), longitude.toString()){
                runBlocking {
                    call.respond(
                        HttpStatusCode.OK,
                        it
                    )
                }
            }
        }
    }
}
