import React, { useEffect, useState } from 'react';
import { View, Text } from 'react-native';
import API from '../lib/api';
import { VictoryBar } from 'victory-native';

export default function AdminDashboard(){
  const [barData, setBarData] = useState<any>({labels:[], values:[]});
  useEffect(()=>{
    API.get('/admin/visuals/bar?surveyId=svy_123&questionId=q3').then(r=>setBarData(r.data)).catch(()=>{});
  },[]);
  return (
    <View style={{flex:1, padding:12}}>
      <Text style={{fontSize:18}}>Admin Dashboard</Text>
      {barData.values && barData.values.length>0 && (
        <VictoryBar data={barData.labels.map((l:any, i:number)=>({x:l, y: barData.values[i]}))} />
      )}
    </View>
  );
}
