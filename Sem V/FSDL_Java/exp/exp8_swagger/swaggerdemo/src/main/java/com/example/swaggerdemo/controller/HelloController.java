package com.example.swaggerdemo.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

@RestController
@RequestMapping("/api/hello")
@Tag(name = "Hello", description = "Greeting APIs")
public class HelloController {

  @GetMapping
  @Operation(summary = "Get default greeting", description = "Returns a static greeting")
  public ResponseEntity<String> hello() {
    return ResponseEntity.ok("Hello from Swagger Demo!");
  }

  @GetMapping("/{name}")
  @Operation(summary = "Get personalized greeting", description = "Returns greeting for provided name")
  public ResponseEntity<String> helloName(@PathVariable String name) {
    return ResponseEntity.ok("Hello, " + name + "!");
  }

  @PostMapping
  @Operation(summary = "Echo message", description = "Accepts message body and echoes it back")
  public ResponseEntity<String> echo(@RequestBody String message) {
    return ResponseEntity.ok("You said: " + message);
  }
}
