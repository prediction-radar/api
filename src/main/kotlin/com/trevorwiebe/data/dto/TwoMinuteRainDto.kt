package com.trevorwiebe.data.dto

import kotlinx.serialization.Serializable

@Serializable
data class TwoMinuteRainDto(
    val date: String,
    val rainAmount: Int,
    val latitude: Float,
    val longitude: Float
)