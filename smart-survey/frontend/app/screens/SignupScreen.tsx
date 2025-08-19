import React, { useState } from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import API from '../lib/api';

export default function SignupScreen({ navigation }: any){
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const signup = async ()=>{
    try{
      await API.post('/auth/signup', { name, email, password });
      alert('Signup successful — please login');
      navigation.goBack();
    }catch(err:any){
      alert(err?.response?.data?.error?.message || 'Signup failed');
    }
  };

  return (
    <View style={{flex:1, padding:12}}>
      <Text style={{fontSize:20}}>Signup</Text>
      <TextInput placeholder="Name" value={name} onChangeText={setName} style={{borderWidth:1, padding:8, marginTop:8}} />
      <TextInput placeholder="Email" value={email} onChangeText={setEmail} style={{borderWidth:1, padding:8, marginTop:8}} />
      <TextInput placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry style={{borderWidth:1, padding:8, marginTop:8}} />
      <Button title="Signup" onPress={signup} />
    </View>
  );
}
