import 'package:flutter/material.dart';
import 'my_webview.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: SafeArea(
        child: Scaffold(
          appBar: null,
          body: MyWebView(
                    title: "DigitalOcean",
                    selectedUrl: "http://10.0.2.2:5000",
        )
        )
      )
    );
  }
}