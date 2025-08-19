import React from 'react';
import { View, Text } from 'react-native';

export default function ThankYou({ route }: any){
  const responseId = route?.params?.responseId;
  return (
    <View style={{flex:1, justifyContent:'center', alignItems:'center', padding:20}}>
      <Text style={{fontSize:20}}>Thanks — response saved!</Text>
      <Text style={{marginTop:8}}>Response ID: {responseId}</Text>
    </View>
  );
}
