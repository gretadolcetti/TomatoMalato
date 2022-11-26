import 'package:flutter/material.dart';
import 'dart:async';
import 'package:flutter_webview_pro/webview_flutter.dart';

class MyWebView extends StatelessWidget {
  final String title;
  final String selectedUrl;

  final Completer<WebViewController> _controller = Completer<WebViewController>();

  MyWebView({
    @required this.title = 'Web View',
    @required this.selectedUrl = 'https://flutter.io',
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: WebView(
        initialUrl: selectedUrl,
        javascriptMode: JavascriptMode.unrestricted,
        onWebViewCreated: (WebViewController webViewController) {
          _controller.complete(webViewController);
        },
      ));
  }
}