package com.ocr.api_server

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class ApiServerApplication

fun main(args: Array<String>) {
	runApplication<ApiServerApplication>(*args)
}
