package com.travelAI.TravelAIdb.vacation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin
@RestController
@RequestMapping("api/v1/vacations")
public class VacationController {
    private final VacationService vacationService;

    @Autowired
    public VacationController(VacationService vacationService) {
        this.vacationService = vacationService;
    }

    // Get all itineraries
    @GetMapping
    public List<Vacation> getVacations() {
        return vacationService.getVacations();
    }

    // Add a new itinerary with JSON data
    @PostMapping
    public void addVacation(@RequestBody String jsonData) {
        // Creating a new Itinerary object with the provided jsonData
        Vacation vacation = new Vacation(jsonData);
        vacationService.addVacation(vacation);
    }

    // Delete an itinerary by ID
    @DeleteMapping(path = "{vacationId}")
    public void deleteVacation(@PathVariable("vacationId") Long vacationId) {
        vacationService.deleteVacation(vacationId);
    }

    // Update an existing itinerary's JSON data
    @PutMapping(path = "{vacationId}")
    public void updateVacation(@PathVariable("vacationId") Long vacationId,
                               @RequestBody String jsonData) {
        vacationService.updateVacation(vacationId, jsonData);
    }
}
