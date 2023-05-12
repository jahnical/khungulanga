import 'package:flutter/material.dart';
import 'package:khungulanga_app/models/disease.dart';
import 'package:khungulanga_app/repositories/disease_repository.dart';

class DiseaseDetailPage extends StatefulWidget {
  final Disease disease;
  final DiseaseRepository diseaseRepository;

  DiseaseDetailPage({required this.disease, required this.diseaseRepository});

  @override
  _DiseaseDetailPageState createState() => _DiseaseDetailPageState();
}

class _DiseaseDetailPageState extends State<DiseaseDetailPage> {
  bool _isLoading = true;
  String? _errorMessage;
  late Disease _disease;

  @override
  void initState() {
    super.initState();
    _loadDisease();
  }

  Future<void> _loadDisease() async {
    try {
      setState(() {
        _isLoading = true;
      });
      final disease = await widget.diseaseRepository.getDiseaseById(widget.disease.id);
      setState(() {
        _disease = disease;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = 'Failed to load disease: $e';
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_isLoading ? 'Loading...' : _errorMessage == null? _disease.name : "Error"),
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return Center(
        child: CircularProgressIndicator(),
      );
    } else if (_errorMessage != null) {
      return _buildError();
    } else {
      return _buildContent();
    }
  }

  Widget _buildContent() {
    return SingleChildScrollView(
      padding: EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            _disease.name,
            style: TextStyle(
              fontSize: 24.0,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 16.0),
          Text(
            _disease.description,
            style: TextStyle(
              fontSize: 16.0,
            ),
          ),
          SizedBox(height: 16.0),
          Text(
            'Severity: ${_disease.severity}',
            style: TextStyle(
              fontSize: 16.0,
            ),
          ),
          SizedBox(height: 16.0),
          Text(
            'Treatments:',
            style: TextStyle(
              fontSize: 16.0,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 8.0),
          ListView.builder(
            shrinkWrap: true,
            itemCount: _disease.treatments.length,
            itemBuilder: (context, index) {
              final treatment = _disease.treatments[index];
              return ListTile(
                title: Text(treatment.title),
                subtitle: Text(treatment.description),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildError() {
    return Center(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              _errorMessage!,
              style: TextStyle(
                fontSize: 16.0,
                color: Colors.red,
              ),
            ),
            SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: _loadDisease,
              child: Text('Retry'),
            ),
          ],
        ),
      )
    );
  }
}
