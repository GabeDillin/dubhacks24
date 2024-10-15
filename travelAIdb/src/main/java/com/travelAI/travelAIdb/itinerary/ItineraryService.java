package com.travelAI.TravelAIdb.itinerary;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class ItineraryService {

    private final ItineraryRepository itineraryRepository;

    @Autowired
    public ItineraryService(ItineraryRepository itineraryRepository){
        this.itineraryRepository = itineraryRepository;
    }

    // Get all itineraries
    public List<Itinerary> getItineraries() {
        return itineraryRepository.findAll();
    }

    // Add a new itinerary with JSON data
    public void addItinerary(Itinerary itinerary) {
        Long itineraryId = itinerary.getId();

        // Check if itinerary already exists
        boolean exists = itineraryRepository.existsById(itineraryId);
        if (exists) {
            throw new IllegalStateException("Itinerary with id " + itineraryId + " already exists");
        }

        // Validate that the JSON data is not null or empty
        String jsonData = itinerary.getJsonData();
        if (jsonData == null || jsonData.trim().isEmpty()) {
            throw new IllegalStateException("Invalid JSON data: It cannot be null or empty.");
        }

        // Save the itinerary
        itineraryRepository.save(itinerary);
    }

    // Delete an itinerary by id
    public void deleteItinerary(Long itineraryId) {
        boolean exists = itineraryRepository.existsById(itineraryId);
        if (!exists) {
            throw new IllegalStateException("Itinerary with id " + itineraryId + " does not exist.");
        }
        itineraryRepository.deleteById(itineraryId);
    }

    // Retrieve a single itinerary by id (optional)
    public Optional<Itinerary> getItineraryById(Long id) {
        return itineraryRepository.findById(id);
    }

    // Update the JSON data for an existing itinerary
    public void updateItinerary(Long id, String jsonData) {
        Itinerary itinerary = itineraryRepository.findById(id).orElseThrow(() ->
                new IllegalStateException("Itinerary with id " + id + " does not exist.")
        );

        // Validate that the JSON data is not null or empty
        if (jsonData == null || jsonData.trim().isEmpty()) {
            throw new IllegalStateException("Invalid JSON data: It cannot be null or empty.");
        }

        // Update the jsonData field and save the itinerary
        itinerary.setJsonData(jsonData);
        itineraryRepository.save(itinerary);
    }
}
