package com.example.employee_dir.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.employee_dir.model.Directory;
import com.example.employee_dir.service.EmployeeService;

@RestController
@RequestMapping("/employees")
public class EmployeeController {

    @Autowired
    private EmployeeService service;

    @GetMapping
    public List<Directory> getEmployees(
            @RequestParam(required = false) String department,
            @RequestParam(required = false, defaultValue = "false") boolean sort) {
        return service.getAllEmployees(department, sort);
    }

    @PostMapping
    public Directory addEmployee(@RequestBody Directory emp) {
        return service.addEmployee(emp);
    }

    @PutMapping("/{id}")
    public Directory updateEmployee(@PathVariable int id, @RequestBody Directory emp) {
        return service.updateEmployee(id, emp);
    }

    @DeleteMapping("/{id}")
    public String deleteEmployee(@PathVariable int id) {
        boolean removed = service.deleteEmployee(id);
        return removed ? "Employee deleted successfully" : "Employee not found";
    }
}
