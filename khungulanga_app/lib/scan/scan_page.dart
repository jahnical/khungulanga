import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import 'extra_info_page.dart';

CameraDescription? camera;
class ScanPage extends StatefulWidget {
  const ScanPage({Key? key}) : super(key: key);

  @override
  _ScanPageState createState() => _ScanPageState();
}

class _ScanPageState extends State<ScanPage> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  bool _flashOn = false;
  bool _cameraInitialized = false;
  XFile? _pickedImage;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    _controller = CameraController(camera!, ResolutionPreset.high);
    _initializeControllerFuture = _controller.initialize();
    _cameraInitialized = true;
    _controller.setFlashMode(FlashMode.off);
  }

  @override
  void dispose() {
    _controller.setFlashMode(FlashMode.off);
    _controller.dispose();
    super.dispose();
  }

  void _toggleFlash() {
    setState(() {
      _flashOn = !_flashOn;
      _controller.setFlashMode(_flashOn ? FlashMode.torch : FlashMode.off);
    });
  }

  void _pickImage() async {
    final pickedImage = await ImagePicker().pickImage(source: ImageSource.gallery);

    if (pickedImage != null) {
      setState(() {
        _pickedImage = XFile(pickedImage.path);
        Navigator.of(context).push(MaterialPageRoute(
            builder: (context) => ExtraInfoPage(imagePath: _pickedImage!.path)));
        //dispose();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_cameraInitialized) {
      return Scaffold(
        body: FutureBuilder<void>(
          future: _initializeControllerFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.done) {
              if (snapshot.hasError) {
                return const Center(
                  child: Text('Failed to initialize camera'),
                );
              } else {
                return Stack(
                  children: [
                    Container(
                      height: double.infinity,
                      width: double.infinity,
                      child: CameraPreview(
                          _controller,
                        child: FittedBox(
                          fit: BoxFit.cover,
                          child: SizedBox(
                            width: _controller.value.previewSize!.height,
                            height: _controller.value.previewSize!.width,
                            child: AspectRatio(
                              aspectRatio: _controller.value.aspectRatio,
                              child: Container(),
                            ),
                          ),
                        ),
                      ),
                    ),
                    Positioned(
                      top: 16,
                      left: 0,
                      right: 0,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          IconButton(
                            onPressed: _toggleFlash,
                            icon: Icon(
                              _flashOn ? Icons.flash_on : Icons.flash_off,
                              color: Colors.white,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Positioned(
                      bottom: 16,
                      left: 80,
                      right: 0,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          FloatingActionButton(
                            onPressed: () async {
                              try {
                                await _initializeControllerFuture;
                                final image = await _controller.takePicture();
                                Navigator.of(context).push(MaterialPageRoute(
                                    builder: (context) => ExtraInfoPage(imagePath: image.path)));
                                //dispose();
                              } catch (e) {
                                // Error handling
                              }
                            },
                            child: const Icon(Icons.camera_alt),
                          ),
                          SizedBox(width: 32),
                          FloatingActionButton(
                            onPressed: _pickImage,
                            child: const Icon(Icons.photo_library),
                          ),
                        ],
                      ),
                    ),
                  ],
                );
              }
            } else {
              return const Center(
                child: CircularProgressIndicator(),
              );
            }
          },
        ),
      );
    } else {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }
  }
}