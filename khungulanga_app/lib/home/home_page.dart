import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:khungulanga_app/appointment/appointment_chats.dart';
import 'package:khungulanga_app/auth/auth/bloc/auth_bloc.dart';
import 'package:khungulanga_app/dermatologists/dermatologists_list.dart';
import 'package:khungulanga_app/diseases/diseases_page.dart';

import '../history/history_page.dart';
import '../scan/scan_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _currentIndex = 0;
  final List<String> _titles = ['History', 'Scan', 'Dermatologists'];

  final List<Widget> _pages = [const HistoryPage(), const ScanPage(), DermatologistList(userLocation: [0.0, 0.0],),];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_titles[_currentIndex]),
        actions: [
          IconButton(
            icon: Icon(Icons.message),
            onPressed: () {
              Navigator.of(context).push(MaterialPageRoute(
                builder: (context) => AppointmentChatsList(),
              ));
            },
          ),
        ],
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(
                color: Theme.of(context).primaryColor,
              ),
              child: const Center(
                child: Text(
                    'KhunguLanga',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    )
                ),
              ),
            ),
            ListTile(
              title: Text('Profile'),
              leading: Icon(Icons.person),
              onTap: () {
                // Navigate to the profile screen
              },
            ),
            ListTile(
              title: Text('Diseases'),
              leading: Icon(Icons.local_hospital),
              onTap: () {
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (context) => DiseasesPage(),
                ));
              },
            ),
            ListTile(
              title: Text('About'),
              leading: Icon(Icons.info),
              onTap: () {
                showDialog(
                  context: context,
                  builder: (BuildContext context) {
                    return AlertDialog(
                      title: Text('Khungulanga'),
                      content: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Version: 1.0.0'),
                          SizedBox(height: 16),
                          Text('Khungulanga is a mobile application that uses machine learning for early skin diagnosis and connects users with dermatologists for expert advice.'),
                          SizedBox(height: 16),
                          Text('Developed by: ICT Group 7'),
                        ],
                      ),
                      actions: [
                        TextButton(
                          onPressed: () {
                            Navigator.pop(context);
                          },
                          child: Text('OK'),
                        ),
                      ],
                    );
                  },
                );
              },
            ),
            ListTile(
              title: Text('Logout'),
              leading: Icon(Icons.logout),
              onTap: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: Text('Logout'),
                    content: Text('Are you sure you want to logout?'),
                    actions: [
                      TextButton(
                        onPressed: () {
                          Navigator.of(context).pop();
                        },
                        child: Text('Cancel'),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          BlocProvider.of<AuthBloc>(context).add(LoggedOut());
                          Navigator.of(context).pop();
                        },
                        child: Text('Logout'),
                      ),
                    ],
                  ),
                );
              },
            ),
          ],
        ),
      ),
      body: _pages[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (int index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.history),
            label: 'History',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.camera_alt, size: 42, color: Colors.purpleAccent,),
            label: 'Scan',
            activeIcon: Icon(Icons.camera_alt, size: 42),
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.people),
            label: 'Dermatologists',
          ),
        ],
      ),
    );
  }
}