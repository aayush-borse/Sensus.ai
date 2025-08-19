import React, { useEffect, useState } from 'react';
import { View, Text, Button, FlatList } from 'react-native';
import API from '../lib/api';
import { getSurveys } from "../api/survey"; // relative path to api folder

const fetchData = async () => {
  const surveys = await getSurveys();
  console.log(surveys);
};


export default function SurveyPicker({ navigation }: any){
  const [surveys, setSurveys] = useState<any[]>([]);

  useEffect(()=>{
    // simple static list for demo; production: API to list active surveys
    setSurveys([{id:'svy_123', title:'Demographic survey'}]);
  },[]);

  return (
    <View style={{flex:1, padding:12}}>
      <Text style={{fontSize:20}}>Choose a survey</Text>
      <FlatList data={surveys} keyExtractor={(i)=>i.id} renderItem={({item})=>(
        <View style={{marginVertical:8}}>
          <Text>{item.title}</Text>
          <Button title="Start" onPress={()=>navigation.navigate('ChatSurvey', { surveyId: item.id })} />
        </View>
      )} />
    </View>
  );
}
