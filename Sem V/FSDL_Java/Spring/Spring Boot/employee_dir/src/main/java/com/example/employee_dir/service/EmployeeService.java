package com.example.employee_dir.service;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.example.employee_dir.model.Directory;

@Service
public class EmployeeService {
    private final Map<Integer, Directory> employees = new HashMap<>();
    private int nextId = 1;

    public List<Directory> getAllEmployees(String department, boolean sortByDept) {
        List<Directory> list = new ArrayList<>(employees.values());

        if (department != null && !department.isEmpty()) {
            list = list.stream()
                       .filter(e -> e.getDepartment().equalsIgnoreCase(department))
                       .collect(Collectors.toList());
        }

        if (sortByDept) {
            list.sort(Comparator.comparing(Directory::getDepartment));
        }

        return list;
    }

    public Directory addEmployee(Directory emp) {
        emp.setId(nextId++);
        employees.put(emp.getId(), emp);
        return emp;
    }

    public Directory updateEmployee(int id, Directory emp) {
        if (employees.containsKey(id)) {
            emp.setId(id);
            employees.put(id, emp);
            return emp;
        }
        return null;
    }

    public boolean deleteEmployee(int id) {
        return employees.remove(id) != null;
    }
}
