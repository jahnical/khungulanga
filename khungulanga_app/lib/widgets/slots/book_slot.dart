import 'package:flutter/material.dart';
import '../../models/dermatologist.dart';
import '../../models/diagnosis.dart';
import '../../models/slot.dart';

class BookSlotPage extends StatelessWidget {
  final Dermatologist? dermatologist;
  final Diagnosis? diagnosis;

  BookSlotPage({this.dermatologist, this.diagnosis});

  List<Slot> slots = [
    Slot(startTime: DateTime(2023, 6, 12, 9, 0), scheduled: false, dermatologistId: 1, dayOfWeek: 1),
    Slot(startTime: DateTime(2023, 6, 12, 10, 0), scheduled: false, dermatologistId: 1, dayOfWeek: 1),
    Slot(startTime: DateTime(2023, 6, 12, 11, 0), scheduled: true, dermatologistId: 1, dayOfWeek: 1),
    Slot(startTime: DateTime(2023, 6, 12, 12, 0), scheduled: false, dermatologistId: 1, dayOfWeek: 1),
    Slot(startTime: DateTime(2023, 6, 12, 13, 0), scheduled: true, dermatologistId: 1, dayOfWeek: 1),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${dermatologist?.user.firstName} ${dermatologist?.user.lastName} Slots'),
      ),
      body: ListView.builder(
        itemCount: slots.length,
        itemBuilder: (BuildContext context, int index) {
          Slot slot = slots[index];
          return ListTile(
            title: Text('Slot ${index + 1}'),
            subtitle: Text('Start Time: ${slot.startTime.toString()}'),
            trailing: slot.scheduled ? Icon(Icons.block, color: Colors.red) : Icon(Icons.check, color: Colors.green),
            onTap: () {
              if (!slot.scheduled) {
// Handle slot booking logic here
                showDialog(
                  context: context,
                  builder: (BuildContext context) {
                    return AlertDialog(
                      title: Text('Book Slot'),
                      content: Text('Do you want to book this slot?'),
                      actions: [
                        TextButton(
                          child: Text('Cancel'),
                          onPressed: () {
                            Navigator.of(context).pop();
                          },
                        ),
                        TextButton(
                          child: Text('Book'),
                          onPressed: () {
// Perform the booking action here
// You can pass the selected slot and diagnosis object to the booking method
                            bookSlot(slot, diagnosis);
                            Navigator.of(context).pop();
                          },
                        ),
                      ],
                    );
                  },
                );
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Slot is already booked.'),
                  ),
                );
              }
            },
          );
        },
      ),
    );
  }

  void bookSlot(Slot slot, Diagnosis? diagnosis) {
// Implement the logic to book the slot here
// You can access the selected slot and diagnosis object and perform the necessary actions
  }
}