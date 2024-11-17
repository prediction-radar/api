package com.trevorwiebe.domain

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.BufferedReader
import java.io.InputStreamReader

class GetRainAmounts{

    suspend operator fun invoke(latitude: String, longitude: String, callback: (String) -> Unit) {

        val command = listOf(
            "python3", "/root/radar-processing-data/get_rainfall_at_location.py", latitude, longitude
        )

        runPythonCommand(command){
            callback(it)
        }
    }

}

private suspend fun runPythonCommand(command: List<String>, callback: (String) -> Unit) {
    withContext(Dispatchers.IO) {
        try {
            val process = ProcessBuilder()
                .command(command)
                .redirectErrorStream(true)
                .start()


            // Read the output of the command
            val reader = BufferedReader(InputStreamReader(process.inputStream))
            val output = StringBuilder()

            var line: String?
            while (reader.readLine().also { line = it } != null) {
                output.append(line).append("\n")
            }

            // Callback with the output when the command has completed
            callback("$output")
        } catch (e: Exception) {
            // Handle exceptions
            callback("Error: ${e.message}")
        }
    }
}