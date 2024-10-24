package com.travelAI.TravelAIdb.vacation;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class VacationService {

    private final VacationRepository vacationRepository;

    @Autowired
    public VacationService(VacationRepository vacationRepository){
        this.vacationRepository = vacationRepository;
    }

    // Get all itineraries
    public List<Vacation> getVacations() {
        return vacationRepository.findAll();
    }

    // Add a new itinerary with JSON data
    public void addVacation(Vacation vacation) {
        Long vacationId = vacation.getId();

        // Check if itinerary already exists
        boolean exists = vacationRepository.existsById(vacationId);
        if (exists) {
            throw new IllegalStateException("Vacation with id " + vacationId + " already exists");
        }

        // Validate that the JSON data is not null or empty
        String jsonData = vacation.getJsonData();
        if (jsonData == null || jsonData.trim().isEmpty()) {
            throw new IllegalStateException("Invalid JSON data: It cannot be null or empty.");
        }
        // Save the itinerary
        vacationRepository.save(vacation);
    }

    // Delete an itinerary by id
    public void deleteVacation(Long vacationId) {
        boolean exists = vacationRepository.existsById(vacationId);
        if (!exists) {
            throw new IllegalStateException("Vacation with id " + vacationId + " does not exist.");
        }
        vacationRepository.deleteById(vacationId);
    }

    // Retrieve a single itinerary by id (optional)
    public Optional<Vacation> getVacationById(Long id) {
        return vacationRepository.findById(id);
    }

    // Update the JSON data for an existing itinerary
    public void updateVacation(Long id, String jsonData) {
        Vacation vacation = vacationRepository.findById(id).orElseThrow(() ->
                new IllegalStateException("Vacation with id " + id + " does not exist.")
        );

        // Validate that the JSON data is not null or empty
        if (jsonData == null || jsonData.trim().isEmpty()) {
            throw new IllegalStateException("Invalid JSON data: It cannot be null or empty.");
        }

        // Update the jsonData field and save the itinerary
        vacation.setJsonData(jsonData);
        vacationRepository.save(vacation);
    }
}
