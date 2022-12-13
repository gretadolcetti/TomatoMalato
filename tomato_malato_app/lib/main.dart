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
                    title: "Tomato Malato",
                    selectedUrl: "http://18.102.4.253",
                    //selectedUrl: "http://10.0.2.2:5000",
        )
        )
      )
    );
  }
}