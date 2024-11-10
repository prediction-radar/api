package com.trevorwiebe.plugins

import com.trevorwiebe.data.dto.TwoMinuteRainDto
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
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
            val utcTime = call.request.queryParameters["utcTime"]
            val latitude = call.request.queryParameters["lat"]?.toFloatOrNull()
            val longitude = call.request.queryParameters["lon"]?.toFloatOrNull()

            if(utcTime == null || latitude == null || longitude == null){
                return@get call.respondText(
                    text = "utcTime, latitude and longitude are both required",
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
