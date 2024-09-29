package com.trevorwiebe.plugins

import com.trevorwiebe.data.dto.TwoMinuteRainDto
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import java.io.File

fun Application.configureRouting() {
    routing {
        get("/tile/{zoom_level}/{x}/{y}") {

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

            val fileName = "/root/radar_data/results/${zoomLevel}_${x}_${y}.png"
            println(fileName)

            val imageFile = File(fileName)

            if (imageFile.exists()) {
                // Set the content type based on your image
                call.response.header(HttpHeaders.ContentType, ContentType.Image.JPEG.toString())
                // Send the image file as a ByteArray
                call.respondBytes(imageFile.readBytes(), ContentType.Image.JPEG)
            } else {
                // Handle the case where the image file doesn't exist
                call.respond(HttpStatusCode.NotFound)
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

            val dummyData = listOf(
                TwoMinuteRainDto(
                    "9/21/2024 21:36",
                    32,
                    latitude,
                    longitude
                ),
                TwoMinuteRainDto(
                    "9/21/2024 21:38",
                    34,
                    latitude,
                    longitude
                )
            )

            call.respond(
                message = dummyData,
                status = HttpStatusCode.OK
            )
        }
    }
}
