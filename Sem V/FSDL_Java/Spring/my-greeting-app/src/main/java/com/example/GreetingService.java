package com.example;

import org.springframework.stereotype.Component;

@Component
public class GreetingService {
    public void getGreeting(){
        System.out.println("Hello Spring Framework!");
    }
}
