import 'package:flutter/material.dart';
import 'package:khungulanga_app/diseases/disease_page.dart';
import 'package:khungulanga_app/models/disease.dart';
import 'package:khungulanga_app/repositories/disease_repository.dart';
import 'package:khungulanga_app/util/common.dart';

class DiseasesPage extends StatefulWidget {
  @override
  _DiseasesPageState createState() => _DiseasesPageState();
}

class _DiseasesPageState extends State<DiseasesPage> {
  late Future<List<Disease>> _diseasesFuture;
  bool _isError = false;

  @override
  void initState() {
    super.initState();
    _diseasesFuture = DiseaseRepository().getDiseases().catchError((_) {
      setState(() {
        _isError = true;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Diseases'),
      ),
      body: Center(
        child: _isError
            ? Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Failed to load diseases. Please check your internet connection and try again.',
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  _diseasesFuture = DiseaseRepository().getDiseases().catchError((_) {
                    setState(() {
                      _isError = true;
                    });
                  });
                  _isError = false;
                });
              },
              child: Text('Retry'),
            ),
          ],
        )
            : FutureBuilder<List<Disease>>(
          future: _diseasesFuture,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              final diseases = snapshot.data!;
              return ListView.builder(
                itemCount: diseases.length,
                itemBuilder: (context, index) {
                  final disease = diseases[index];
                  return Container(
                    decoration: BoxDecoration(
                      border: Border(bottom: BorderSide(color: Colors.grey.shade300)),
                    ),
                    child: ListTile(
                      leading: Icon(Icons.local_hospital, color: Colors.blue),
                      title: Text(toTitleCase(disease.name)),
                      subtitle: Text(
                        'Severity: ${disease.severity}',
                        style: TextStyle(
                          fontWeight: FontWeight.w400,
                          color: Colors.grey.shade600,
                        ),
                      ),
                      trailing: Icon(Icons.arrow_forward_ios_rounded),
                      onTap: () {
                        Navigator.of(context).push(MaterialPageRoute(
                          builder: (context) => DiseaseDetailPage(disease: disease, diseaseRepository: DiseaseRepository()),
                        ));
                      },
                    ),
                  );
                },
              );
            } else if (snapshot.hasError) {
              return Text('Failed to load diseases. Please check your internet connection and try again.');
            }
            return CircularProgressIndicator();
          },
        ),
      ),
    );
  }
}