import 'dart:developer';
import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:khungulanga_app/repositories/diagnosis_repository.dart';

import '../diagnosis/diagnosis_page.dart';

class ExtraInfoPage extends StatefulWidget {
  final String imagePath;

  const ExtraInfoPage({required this.imagePath, Key? key}) : super(key: key);

  @override
  _ExtraInfoPageState createState() => _ExtraInfoPageState();
}

class _ExtraInfoPageState extends State<ExtraInfoPage> {
  final _formKey = GlobalKey<FormState>();
  String? _selectedBodyPart = "Face";
  bool _isItchy = false;
  bool _isLoading = false;

  void _submitForm() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      setState(() {
        _isLoading = true;
      });

      final formData = FormData.fromMap({
        'body_part': _selectedBodyPart,
        'itchy': _isItchy,
        'image': await MultipartFile.fromFile(widget.imagePath),
      });

      try {
        final diagnosis = await DiagnosisRepository().diagnose(formData);
        setState(() {
          _isLoading = false;
        });
        // Navigate to the success page
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (context) => DiagnosisPage(
              diagnosis: diagnosis,
            ),
          ),
        );
      } catch (e) {
        // Handle error
        log("Error", error: e);
        setState(() {
          _isLoading = false;
        });
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Error'),
            content: Text(e.toString().substring(11).replaceAll(")", "")),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('OK'),
              ),
            ],
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Diagnosis Info')),
      body: Column(
        children: [
          Expanded(
            child: Image.file(
              File(widget.imagePath),
              fit: BoxFit.cover,
              width: double.infinity,
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const SizedBox(height: 2.0),
                  const Text(
                    'Select body part:',
                    style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w400),
                  ),
                  const SizedBox(height: 2.0),
                  DropdownButtonFormField<String>(
                    value: _selectedBodyPart,
                    items: const [
                      DropdownMenuItem(
                        value: 'Face',
                        child: Text('Face'),
                      ),
                      DropdownMenuItem(
                        value: 'Upper Body',
                        child: Text('Upper Body'),
                      ),
                      DropdownMenuItem(
                        value: 'Arms Hands',
                        child: Text('Arms or Hands')
                      ),
                      DropdownMenuItem(
                        value: 'Legs Feet',
                        child: Text('Feet or Legs'),
                      ),
                    ],
                    onChanged: (value) {
                      setState(() {
                        _selectedBodyPart = value;
                      });
                    },
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      isDense: true,
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please select a body part';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16.0),
                  const Text(
                    'Is it itchy?',
                    style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w400),
                  ),
                  const SizedBox(height: 0.0),
                  SwitchListTile(
                    value: _isItchy,
                    onChanged: (value) {
                      setState(() {
                        _isItchy = value;
                      });
                    },
                    title: Text(_isItchy ? 'Yes' : 'No'),
                  ),
                  const SizedBox(height: 24.0),
                  ElevatedButton(
                    onPressed: _isLoading ? null : _submitForm,
                    style: ButtonStyle(
                      fixedSize: MaterialStateProperty.all<Size>(
                        const Size(double.infinity, 60), // Set desired height here
                      ),
                    ),
                    child: _isLoading ? const CircularProgressIndicator() : const Text('Diagnose'),
                  ),
                  const SizedBox(height: 8.0),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
