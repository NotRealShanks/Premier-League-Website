package com.github.notrealshanks.pl.premierzone.player.model;

import jakarta.persistence.*;

@Entity
@Table(name="player_stats")
public class Player {
    @Id
    @Column(name="player_name") // Matches player_name VARCHAR(100)
    private String name;

    @Column(name="nation") // Matches nation VARCHAR(50)
    private String nation;

    @Column(name="position") // Matches position VARCHAR(50)
    private String pos;

    @Column(name="age") // Matches age INTEGER
    private Integer age;

    @Column(name="matches_played") // Matches matches_played INTEGER
    private Integer mp;

    @Column(name="starts") // Matches starts INTEGER
    private Integer starts;

    @Column(name="minutes_played") // Matches minutes_played FLOAT
    private Double min;

    @Column(name="goals") // Matches goals FLOAT
    private Double gls;

    @Column(name="assists") // Matches assists FLOAT
    private Double ast;

    @Column(name="penalties_scored") // Matches penalties_scored FLOAT
    private Double pk;

    @Column(name="yellow_cards") // Matches yellow_cards FLOAT
    private Double crdy;

    @Column(name="red_cards") // Matches red_cards FLOAT
    private Double crdr;

    @Column(name="expected_goals") // Matches expected_goals FLOAT
    private Double xg;

    @Column(name="expected_assists") // Matches expected_assists FLOAT
    private Double xag;

    @Column(name="team_name") // Matches team_name VARCHAR(100)
    private String team;

    public Player() {
    }

    public Player(String name, String nation, String pos, Integer age, Integer mp, Integer starts, Double min, Double gls, Double ast, Double pk, Double crdy, Double crdr, Double xg, Double xag, String team) {
        this.name = name;
        this.nation = nation;
        this.pos = pos;
        this.age = age;
        this.mp = mp;
        this.starts = starts;
        this.min = min;
        this.gls = gls;
        this.ast = ast;
        this.pk = pk;
        this.crdy = crdy;
        this.crdr = crdr;
        this.xg = xg;
        this.xag = xag;
        this.team = team;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getNation() {
        return nation;
    }

    public void setNation(String nation) {
        this.nation = nation;
    }

    public String getPos() {
        return pos;
    }

    public void setPos(String pos) {
        this.pos = pos;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Integer getMp() {
        return mp;
    }

    public void setMp(Integer mp) {
        this.mp = mp;
    }

    public Integer getStarts() {
        return starts;
    }

    public void setStarts(Integer starts) {
        this.starts = starts;
    }

    public Double getMin() {
        return min;
    }

    public void setMin(Double min) {
        this.min = min;
    }

    public Double getGls() {
        return gls;
    }

    public void setGls(Double gls) {
        this.gls = gls;
    }

    public Double getAst() {
        return ast;
    }

    public void setAst(Double ast) {
        this.ast = ast;
    }

    public Double getPk() {
        return pk;
    }

    public void setPk(Double pk) {
        this.pk = pk;
    }

    public Double getCrdy() {
        return crdy;
    }

    public void setCrdy(Double crdy) {
        this.crdy = crdy;
    }

    public Double getCrdr() {
        return crdr;
    }

    public void setCrdr(Double crdr) {
        this.crdr = crdr;
    }

    public Double getXg() {
        return xg;
    }

    public void setXg(Double xg) {
        this.xg = xg;
    }

    public Double getXag() {
        return xag;
    }

    public void setXag(Double xag) {
        this.xag = xag;
    }

    public String getTeam() {
        return team;
    }

    public void setTeam(String team) {
        this.team = team;
    }
}
